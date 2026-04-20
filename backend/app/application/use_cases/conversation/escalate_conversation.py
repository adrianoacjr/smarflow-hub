from domain.entities.conversation import Conversation
from domain.interfaces.conversation_repository import IConversationRepository
from application.dtos.conversation.escalate_conversation_command import EscalateConversationCommand
from application.exceptions.conversation_exceptions import (
    ConversationNotFoundError,
    ConversationInvalidTransitionError
)

class EscalateConversation:
    def __init__(self, conversation_repo: IConversationRepository) -> None:
        self.conversation_repo = conversation_repo

    async def execute(self, command: EscalateConversationCommand) -> Conversation:
        conversation = await self.conversation_repo.get_by_id(command.conversation_id)
        if conversation is None:
            raise ConversationNotFoundError(f"Conversation '{command.conversation_id}' not found")
        try:
            conversation.escalate(reason=command.reason)
        except ValueError as exc:
            raise ConversationInvalidTransitionError(str(exc)) from exc
        
        return await self.conversation_repo.update(conversation)
