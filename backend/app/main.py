from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.controllers import user_routes
from infrastructure.controllers import message_routes
from infrastructure.controllers import customer_routes
from infrastructure.controllers import auth_routes
from infrastructure.controllers import health_routes
from infrastructure.controllers import test_db_router
from infrastructure.controllers import webhook_whatsapp_routes
from infrastructure.controllers import gpt_routes

app = FastAPI(title="SmartFlow Hub API")

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
app.include_router(customer_routes.router)
app.include_router(message_routes.router)
app.include_router(auth_routes.router)
app.include_router(webhook_whatsapp_routes.router, prefix="/webhooks")
app.include_router(health_routes.router)
app.include_router(test_db_router.router, prefix="/health")
app.include_router(gpt_routes.router, tags=["AI"])
