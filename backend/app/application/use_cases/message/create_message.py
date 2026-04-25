from uuid import uuid4
from domain.utils.time import utcnow

from domain.entities.message import Message
from domain.enums.message_direction import MessageDirection
from domain.enums.message_status import MessageStatus
from domain.interfaces.customer_repository import ICustomerRepository
from domain.interfaces.message_repository import IMessageRepository
from domain.interfaces.user_repository import IUserRepository
from domain.value_objects.message_content import MessageContent
from application.dtos.message.create_message_command import CreateMessageCommand
from application.exceptions.message_exceptions import (
    CustomerNotFoundError,
    UserNotFoundError
)

class CreateMessage:
    def __init__(
        self,
        message_repo: IMessageRepository,
        customer_repo: ICustomerRepository,
        user_repo: IUserRepository,
    ) -> None:
        self.message_repo = message_repo
        self.customer_repo = customer_repo
        self.user_repo = user_repo

    async def execute(self, command: CreateMessageCommand) -> Message:
        customer = await self.customer_repo.get_by_id(command.customer_id)
        if customer is None:
            raise CustomerNotFoundError("Customer not found")
        
        user = await self.user_repo.get_by_id(command.user_id)
        if user is None:
            raise UserNotFoundError("User not found")
        
        content = MessageContent(command.content)

        message = Message(
            id=uuid4(),
            customer_id=command.customer_id,
            user_id=command.user_id,
            content=content,
            direction=command.direction,
            source=command.source,
            created_at=utcnow(),
            automated=command.automated,
            status=self._define_initial_status(command.direction),
        )

        return await self.message_repo.create(message)
    
    def _define_initial_status(self, direction: MessageDirection) -> MessageStatus:
        if direction == MessageDirection.INBOUND:
            return MessageStatus.RECEIVED
        
        return MessageStatus.PENDING
