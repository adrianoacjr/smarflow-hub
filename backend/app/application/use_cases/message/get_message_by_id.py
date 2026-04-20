from uuid import UUID

from domain.entities.message import Message
from domain.interfaces.message_repository import IMessageRepository
from application.exceptions.message_exceptions import MessageNotFoundError

class GetMessageById:
    def __init__(self, message_repo: IMessageRepository) -> None:
        self.message_repo = message_repo

    async def execute(self, message_id: UUID) -> Message:
        message = await self.message_repo.get_by_id(message_id)
        if message is None:
            raise MessageNotFoundError(f"Message '{message_id}' not found")
        return message
