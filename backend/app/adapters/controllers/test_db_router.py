from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
# from core.database import get_session

def build_db_router(
    session: AsyncSession
) -> APIRouter:
    router = APIRouter()

    @router.get("/db-check")
    async def db_check():
        try:
            result = await session.execute(text("SELECT 1;"))
            value = result.scalar()
            return {"database": "connected", "result": value}
        except Exception as e:
            return {"database": "error", "detail": str(e)}

    return router
