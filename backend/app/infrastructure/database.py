from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from infrastructure.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    future=True,
    echo=True
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

@asynccontextmanager
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
