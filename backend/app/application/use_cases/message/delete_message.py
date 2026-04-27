from uuid import UUID

from domain.interfaces.message_repository import IMessageRepository
from application.exceptions.message_exceptions import MessageNotFoundError

class DeleteMessage:
    def __init__(self, message_repo: IMessageRepository) -> None:
        self.message_repo = message_repo

    async def execute(self, message_id: UUID) -> None:
        message=await self.message_repo.get_by_id(message_id)
        if message is None:
            raise MessageNotFoundError(f"Message '{message_id}' not found")
        await self.message_repo.delete(message_id)
