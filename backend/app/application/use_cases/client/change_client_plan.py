from domain.entities.client import Client
from domain.enums.client_plan import ClientPlan
from domain.interfaces.client_repository import IClientRepository
from application.exceptions.client_exceptions import (
    ClientNotFoundError,
    ClientInactiveError,
)

class ChangeClientPlan:
    def __init__(self, repo: IClientRepository) -> None:
        self.repo = repo

    async def execute(self, client_id: int, new_plan: ClientPlan) -> Client:
        client = await self.repo.get_by_id(client_id)
        if client is None:
            raise ClientNotFoundError(f"Client '{client_id}' not found.")
        if not client.active:
            raise ClientInactiveError(
                f"Cannot change plan of inactive client '{client_id}'."
            )
        
        client.change_plan(new_plan)
        return await self.repo.update(client)
