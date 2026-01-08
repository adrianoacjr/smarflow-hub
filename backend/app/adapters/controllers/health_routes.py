from fastapi import APIRouter

def build_health_router():
    router = APIRouter()

    @router.get("/health")
    def check_system_health():
        return {"status": "ok"}
