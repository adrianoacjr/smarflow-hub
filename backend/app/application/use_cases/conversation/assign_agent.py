from domain.entities.conversation import Conversation
from domain.enums.user_type import UserType
from domain.interfaces.conversation_repository import IConversationRepository
from domain.interfaces.user_repository import IUserRepository
from application.dtos.conversation.assign_agent_command import AssignAgentCommand
from application.exceptions.conversation_exceptions import (
    ConversationNotFoundError,
    ConversationInvalidTransitionError,
    AgentNotAvailableError,
)
from application.exceptions.message_exceptions import UserNotFoundError

class AssignAgent:
    def __init__(
        self,
        conversation_repo: IConversationRepository,
        user_repo: IUserRepository,
    ) -> None:
        self.conversation_repo = conversation_repo
        self.user_repo = user_repo

    async def execute(self, command: AssignAgentCommand) -> Conversation:
        conversation = await self.conversation_repo.get_by_id(command.conversation_id)
        if conversation is None:
            raise ConversationInvalidTransitionError(f"Conversation '{command.conversation_id}' not found")
        
        agent = await self.user_repo.get_by_id(command.agent_id)
        if agent is None:
            raise UserNotFoundError(f"Agent '{command.agent_id}' not found")
        if agent.is_bot:
            raise AgentNotAvailableError("Cannot assign a bot as a human agent")
        if not agent.active:
            raise AgentNotAvailableError(f"Agent '{command.agent_id}' is inactive")
        
        try:
            conversation.assigned_agent(command.agent_id)
        except ValueError as exc:
            raise ConversationInvalidTransitionError(str(exc)) from exc
        
        return await self.conversation_repo.update(conversation)
