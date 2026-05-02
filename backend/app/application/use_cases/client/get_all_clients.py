from domain.interfaces.client_repository import IClientRepository
from application.dtos.client.list_clients_query import ListClientQuery

class GetAllClients:
    def __init__(self, repo: IClientRepository) -> None:
        self.repo = repo

    async def execute(self, limit: int = 50, offset: int = 0) -> ListClientQuery:
        items = await self.repo.list(limit=limit, offset=offset)
        total = await self.repo.count()
        return ListClientQuery(
            items=tuple(items),
            total=total,
            limit=limit,
            offset=offset,
        )
