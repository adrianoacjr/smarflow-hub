from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from adapters.controllers.health_routes import build_health_router
from adapters.controllers.auth_routes import router as auth_router
from adapters.controllers.user_routes import router as user_router
from adapters.controllers.customer_routes import router as customer_router
from adapters.controllers.message_routes import router as message_router
from adapters.controllers.webhook_whatsapp_routes import router as webhook_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="SmartFlow Hub API",
    version="0.1.0",
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

app.include_router(build_health_router())
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(customer_router)
app.include_router(message_router)
app.include_router(webhook_router)
