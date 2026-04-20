from uuid import UUID

from domain.entities.conversation import Conversation
from domain.enums.conversation_status import ConversationStatus
from domain.interfaces.conversation_repository import IConversationRepository
from application.exceptions.conversation_exceptions import (
    ConversationNotFoundError,
    ConversationInvalidTransitionError
)

class ResolveConversation:
    def __init__(self, conversation_repo: IConversationRepository) -> None:
        self.conversation_repo = conversation_repo

    async def execute(self, conversation_id: UUID) -> Conversation:
        conversation = await self.conversation_repo.get_by_id(conversation_id)
        if conversation is None:
            raise ConversationNotFoundError(f"Conversation '{conversation_id}' not found")
        if conversation.status == ConversationStatus.RESOLVED:
            raise ConversationInvalidTransitionError(f"Conversation '{conversation_id}' is already resolved")
        
        conversation.resolve()
        return await self.conversation_repo.update(conversation)
