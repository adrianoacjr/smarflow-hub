from application.dtos.message.update_message_status_command import UpdateMessageStatusCommand
from application.exceptions.message_exceptions import (
    InvalidMessageStatusTransitionError,
    MessageNotFoundError,
)
from domain.entities.message import Message
from domain.interfaces.message_repository import IMessageRepository

class UpdateMessageStatus:
    def __init__(self, message_repo: IMessageRepository) -> None:
        self.message_repo = message_repo

    async def execute(self, command: UpdateMessageStatusCommand) -> Message:
        message = await self.message_repo.get_by_id(command.message_id)
        if message is None:
            raise MessageNotFoundError("Message not found")
        
        try:
            message.update_status(command.status)
        except ValueError as exc:
            raise InvalidMessageStatusTransitionError(str(exc)) from exc
        
        return await self.message_repo.update(message)
