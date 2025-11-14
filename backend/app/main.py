from presentation.controllers import user_routes, message_routes, auth_routes
from fastapi import FastAPI

app = FastAPI(title="SmartFlow Hub API")
app.include_router(user_routes.router)
app.include_router(message_routes.router)
app.include_router(auth_routes.router)
