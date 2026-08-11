from uuid import UUID

from domain.entities.client import Client
from domain.interfaces.client_repository import IClientRepository
from application.exceptions.client_exceptions import (
    ClientNotFoundError,
    ClientInactiveError,
)

class DeactivateClient:
    def __init__(self, repo: IClientRepository) -> None:
        self.repo = repo

    async def execute(self, client_id: UUID) -> Client:
        client = await self.repo.get_by_id(client_id)

        if client is None:
            raise ClientNotFoundError(f"Client '{client_id}' not found.")

        if not client.active:
            raise ClientInactiveError(
                f"Client '{client_id}' is already inactive."
            )

        client.deactivate()

        return await self.repo.update(client)
