from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import get_session

from infrastructure.dependencies.di_user import di_user
from infrastructure.dependencies.di_message import di_message
from infrastructure.dependencies.di_customer import di_customer
from infrastructure.dependencies.di_auth import di_auth
from infrastructure.dependencies.di_ai import di_ai

from adapters.controllers.user_routes import build_user_router
from adapters.controllers.message_routes import build_message_router
from adapters.controllers.customer_routes import build_customer_router
from adapters.controllers.auth_routes import build_auth_router
from adapters.controllers.health_routes import build_health_router
from adapters.controllers.test_db_router import build_db_router
from adapters.controllers.webhook_whatsapp_routes import build_webhook_whatsapp_router
from adapters.controllers.gpt_routes import build_gpt_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with get_session() as session:
        (
            create_user,
            get_user,
            get_all_users,
            delete_user,
        ) = di_user.build(session)

        user_router = build_user_router(
            create_user=create_user,
            get_user=get_user,
            get_all_users=get_all_users,
            delete_user=delete_user,
        )

        app.include_router(user_router)

        (
            receive_whatsapp_message,
            create_message,
            get_message_by_id,
            list_message_by_user,
            list_message_by_customer,
            delete_message,
        ) = di_message.build(session)

        message_router = build_message_router(
            receive_whatsapp_message=receive_whatsapp_message,
            create_message=create_message,
            get_message_by_id=get_message_by_id,
            list_message_by_user=list_message_by_user,
            list_message_by_customer=list_message_by_customer,
            delete_message=delete_message,
        )

        app.include_router(message_router)

        yield

app = FastAPI(
    title="SmartFlow Hub API",
    lifespan=lifespan,
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customer_routes.router)
app.include_router(auth_routes.router)
app.include_router(webhook_whatsapp_routes.router, prefix="/webhooks")
app.include_router(health_routes.router)
app.include_router(test_db_router.router, prefix="/health")
app.include_router(gpt_routes.router, tags=["AI"])
