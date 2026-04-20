from domain.entities.message import Message
from domain.enums.message_direction import MessageDirection
from domain.enums.message_status import MessageStatus
from domain.interfaces.message_repository import IMessageRepository
from application.dtos.message.send_message_command import SendMessageCommand
from application.exceptions.message_exceptions import (
    InvalidMessageFlowError,
    MessageNotFoundError,
)
from application.interfaces.message_sender import IMessageSender

class SendMessage:
    def __init__(
        self,
        message_repo: IMessageRepository,
        message_sender: IMessageSender,
    ) -> None:
        self.message_repo = message_repo
        self.message_sender = message_sender

    async def execute(self, command: SendMessageCommand) -> Message:
        message = await self.message_repo.get_by_id(command.message_id)
        if message is None:
            raise MessageNotFoundError("Message not found")
        
        if message.direction != MessageDirection.OUTBOUND:
            raise InvalidMessageFlowError("Only outbound messages can be sent")
        
        if message.status != MessageStatus.PENDING:
            raise InvalidMessageFlowError("Only pending messages can be sent")
        
        try:
            await self.message_sender.send(message)
            message.mark_as_sent()
        except Exception as exc:
            message.mark_as_failed()
            await self.message_repo.update(message)
            raise exc
        
        return await self.message_repo.update(message)
