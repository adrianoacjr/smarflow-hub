from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.dependencies.di_user import di_user
from infrastructure.dependencies.di_message import di_message
from infrastructure.dependencies.di_customer import di_customer
from infrastructure.dependencies.di_auth import di_auth
from infrastructure.dependencies.di_ai import di_ai
from adapters.controllers import user_routes
from adapters.controllers.message_routes import build_message_router
from adapters.controllers.customer_routes import build_customer_router
from adapters.controllers.auth_routes import build_auth_router
from adapters.controllers.health_routes import build_health_router
from adapters.controllers.test_db_router import build_db_router
from adapters.controllers.webhook_whatsapp_routes import build_webhook_whatsapp_router
from adapters.controllers.gpt_routes import build_gpt_router
from infrastructure.database import get_session

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with get_session() as session:
        (
            receive_whatsapp_message,
            create_message,
            get_message_by_id,
            list_message_by_user,
            list_message_by_customer,
            delete_message,
        ) = di_message.build(session)

        message_router = build_message_router(
            create_message=create_message,
            get_message_by_id=get_message_by_id,
            list_message_by_user=list_message_by_user,
            list_message_by_customer=list_message_by_customer,
            delete_message=delete_message,
        )

        app.include_router(message_router)

        webhook_whatsapp_router = build_webhook_whatsapp_router(
            receive_whatsapp_message=receive_whatsapp_message,
        )

        app.include_router(webhook_whatsapp_router, prefix="/webhooks")

        (
            create_customer,
            delete_customer,
            get_all_customers,
            get_customer,
            update_customer,
        ) = di_customer.build(session)

        customer_router = build_customer_router(
            create_customer=create_customer,
            delete_customer=delete_customer,
            get_all_customers=get_all_customers,
            get_customer=get_customer,
            update_customer=update_customer,
        )

        app.include_router(customer_router)

        authenticate_user = di_auth.build(session)

        auth_router = build_auth_router(
            authenticate_user=authenticate_user,
        )

        app.include_router(auth_router)

        health_router = build_health_router()

        app.include_router(health_router)

        test_db_router = build_db_router(
            session=session,
        )

        app.include_router(test_db_router, prefix="/health")

        process_ai_reply = di_ai.build(session)

        gpt_routes = build_gpt_router(
            process_ai_reply=process_ai_reply,
        )

        app.include_router(gpt_routes, tags=["AI"])

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

app.include_router(user_routes.router)
