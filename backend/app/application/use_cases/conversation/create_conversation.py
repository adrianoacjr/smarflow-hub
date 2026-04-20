from datetime import datetime, timezone
from uuid import uuid4

from domain.entities.conversation import Conversation
from domain.enums.conversation_status import ConversationStatus
from domain.interfaces.conversation_repository import IConversationRepository
from domain.interfaces.customer_repository import ICustomerRepository
from domain.interfaces.user_repository import IUserRepository
from application.dtos.conversation.create_conversation_command import CreateConversationCommand
from application.exceptions.message_exceptions import (
    CustomerNotFoundError,
    UserNotFoundError
)

class CreateConversation:
    def __init__(
        self,
        conversation_repo: IConversationRepository,
        customer_repo: ICustomerRepository,
        user_repo: IUserRepository,
    ) -> None:
        self.conversation_repo = conversation_repo
        self.customer_repo = customer_repo
        self.user_repo = user_repo
    
    async def execute(self, command: CreateConversationCommand) -> Conversation:
        customer = await self.customer_repo.get_by_id(command.customer_id)
        if customer is None:
            raise CustomerNotFoundError(f"Customer '{command.customer_id}' not found")
        
        bot = await self.user_repo.get_by_id(command.bot_user_id)
        if bot is None:
            raise UserNotFoundError(f"Bot user '{command.bot_user_id}' bot found")
        if not bot.is_bot:
            raise ValueError(f"User '{command.bot_user_id}' is not a bot")
        
        existing = await self.conversation_repo.get_active_by_customer(
            customer_id = command.customer_id,
            source = command.source
        )
        if existing is not None:
            return existing
        
        now = datetime.now(timezone.utc)
        conversation = Conversation(
            id = uuid4(),
            customer_id = command.customer_id,
            bot_user_id = command.bot_user_id,
            source = command.source,
            status = ConversationStatus.BOT_HANDLING,
            created_at = now,
            updated_at = now,
        )
        return await self.conversation_repo.create(conversation)
