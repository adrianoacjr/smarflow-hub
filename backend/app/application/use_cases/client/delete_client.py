from domain.interfaces.client_repository import IClientRepository
from application.exceptions.client_exceptions import ClientNotFoundError

class DeleteClient:
    def __init__(self, repo: IClientRepository) -> None:
        self.repo = repo

    async def execute(self, client_id: int) -> None:
        deleted = await self.repo.delete(client_id)
        if not deleted:
            raise ClientNotFoundError(f"Client '{client_id}' not found.")
