from domain.interfaces.client_repository import IClientRepository
from application.dtos.client.client_item import ClientItem
from application.dtos.client.list_clients_query import ListClientQuery
from application.dtos.client.list_clients_result import ListClientsResult

class GetAllClients:
    def __init__(self, repo: IClientRepository) -> None:
        self.repo = repo

    async def execute(self, query: ListClientQuery) -> ListClientsResult:
        clients = await self.repo.list(
            limit=query.limit,
            offset=query.offset,
        )

        total = await self.repo.count()

        return ListClientsResult(
            items=tuple(
                ClientItem.from_entity(client)
                for client in clients
            ),
            total=total,
            limit=query.limit,
            offset=query.offset,
        )
