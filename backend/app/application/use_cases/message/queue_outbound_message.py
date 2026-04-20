from datetime import datetime, timezone
from uuid import uuid4

from domain.entities.message import Message
from domain.enums.message_direction import MessageDirection
from domain.enums.message_status import MessageStatus
from domain.interfaces.customer_repository import ICustomerRepository
from domain.interfaces.message_repository import IMessageRepository
from domain.interfaces.user_repository import IUserRepository
from domain.value_objects.message_content import MessageContent
from application.dtos.message.queue_outbound_message_command import QueueOutboundMessageCommand
from application.exceptions.message_exceptions import (
    CustomerNotFoundError,
    UserNotFoundError
)

class QueueOutboundMessage:
    def __init__(
        self,
        message_repo: IMessageRepository,
        customer_repo: ICustomerRepository,
        user_repo: IUserRepository
    ) -> None:
        self.message_repo = message_repo
        self.customer_repo = customer_repo
        self.user_repo = user_repo

    async def execute(self, command: QueueOutboundMessageCommand) -> Message:
        customer = await self.customer_repo.get_by_id(command.customer_id)
        if customer is None:
            raise CustomerNotFoundError("Customer not found")
        
        user = await self.user_repo.get_by_id(command.user_id)
        if user is None:
            raise UserNotFoundError("User not found")
        
        message = Message(
            id = uuid4(),
            customer_id = command.customer_id,
            user_id = command.user_id,
            content = MessageContent(command.content),
            direction = MessageDirection.OUTBOUND,
            source = command.source,
            created_at = datetime.now(timezone.utc),
            automated = command.automated,
            status = MessageStatus.PENDING
        )

        return await self.message_repo.create(message)
