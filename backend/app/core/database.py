from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    furute=True,
    echo=True
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
