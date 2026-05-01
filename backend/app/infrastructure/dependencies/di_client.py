from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.repositories.client_repository_postgres import (
    ClientRepositoryPostgres,
)

def get_client_repository(session: AsyncSession) -> ClientRepositoryPostgres:
    return ClientRepositoryPostgres(session)
