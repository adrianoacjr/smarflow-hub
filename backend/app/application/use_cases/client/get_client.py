from uuid import UUID

from domain.interfaces.client_repository import IClientRepository
from application.dtos.client.client_item import ClientItem
from application.exceptions.client_exceptions import ClientNotFoundError

class GetClient:
    def __init__(self, repo: IClientRepository) -> None:
        self.repo = repo

    async def execute(self, client_id: UUID) -> ClientItem:
        client = await self.repo.get_by_id(client_id)

        if client is None:
            raise ClientNotFoundError(f"Client '{client_id}' not found.")
        return ClientItem.from_entity(client)
