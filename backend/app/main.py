from presentation.controllers import user_routes, message_routes, auth_routes, whatsapp_webhook, health_routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SmartFlow Hub API")

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

app.include_router(user_routes.router)
app.include_router(message_routes.router)
app.include_router(auth_routes.router)
app.include_router(whatsapp_webhook.router, prefix="/webhooks")
app.include_router(health_routes.router)
