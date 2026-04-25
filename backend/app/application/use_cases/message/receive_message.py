from datetime import datetime, timezone
from uuid import uuid4

from domain.entities.message import Message, MessageAttachment
from domain.enums.message_direction import MessageDirection
from domain.enums.message_status import MessageStatus
from domain.interfaces.message_repository import IMessageRepository
from domain.interfaces.user_repository import IUserRepository
from domain.value_objects.message_content import MessageContent
from application.dtos.message.receive_message_command import ReceiveMessageCommand
from application.exceptions.message_exceptions import (
    MessageValidationError,
    UserNotFoundError
)
from application.use_cases.customer.get_or_create_customer import GetOrCreateCustomer

class ReceiveMessage:
    def __init__(
        self,
        message_repo: IMessageRepository,
        user_repo: IUserRepository,
        get_or_create_customer: GetOrCreateCustomer,
    ) -> None:
        self.message_repo = message_repo
        self.user_repo = user_repo
        self.get_or_create_customer = get_or_create_customer

    async def execute(self, command: ReceiveMessageCommand) -> Message:
        user = await self.user_repo.get_by_id(command.user_id)
        if user is None:
            raise UserNotFoundError("User not found")
        
        customer = await self.get_or_create_customer.execute(
            source=command.source,
            source_customer_ref=command.source_customer_ref,
            name=command.customer_name
        )

        if not command.content and not command.attachments:
            raise MessageValidationError("Message must have content or attachments")
        
        attachments = tuple(
            MessageAttachment(
                url=item.url,
                mime_type=item.mime_type,
                filename=item.filename,
            )
            for item in command.attachments
        )
        
        message = Message(
            id = uuid4(),
            customer_id=customer.id,
            user_id=command.user_id,
            content=MessageContent(command.content) if command.content else None,
            direction=MessageDirection.INBOUND,
            source=command.source,
            created_at=datetime.now(timezone.utc),
            automated=command.automated,
            status=MessageStatus.RECEIVED,
            attachments=attachments,
        )

        return await self.message_repo.create(message)
