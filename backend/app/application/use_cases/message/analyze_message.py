from uuid import UUID

from domain.constants.conversation import (
    AI_CONFIDENCE_THRESHOLD,
    CONVERSATION_HISTORY_SIZE,
    HUMAN_ESCALATION_TRIGGERS
)
from domain.entities.message import Message
from domain.enums.message_direction import MessageDirection
from domain.enums.message_status import MessageStatus
from domain.interfaces.message_repository import IMessageRepository
from application.dtos.conversation.create_conversation_command import CreateConversationCommand
from application.dtos.conversation.escalate_conversation_command import EscalateConversationCommand
from application.dtos.message.analyze_message_command import AnalyzeMessageCommand
from application.dtos.message.analyze_message_result import AnalyzeMessageResult, AnalysisOutcome
from application.use_cases.conversation.create_conversation import CreateConversation
from application.use_cases.conversation.escalate_conversation import EscalateConversation
from application.dtos.message.queue_outbound_message_command import QueueOutboundMessageCommand
from application.exceptions.message_exceptions import MessageNotFoundError
from application.interfaces.ai_responder_gateway import IAIResponderGateway
from application.use_cases.message.queue_outbound_message import QueueOutboundMessage

class AnalyzeMessage:
    def __init__(
        self,
        message_repo: IMessageRepository,
        ai_gateway: IAIResponderGateway,
        queue_outbound: QueueOutboundMessage,
        create_conversation: CreateConversation,
        escalate_conversation: EscalateConversation,
    ) -> None:
        self.message_repo = message_repo
        self.ai_gateway = ai_gateway
        self.queue_outbound = queue_outbound
        self.create_conversation = create_conversation
        self.escalate_conversation = escalate_conversation

    async def execute(self, command: AnalyzeMessageCommand) -> AnalyzeMessageResult:
        inbound = await self.message_repo.get_by_id(command.inbound_message_id)
        if inbound is None:
            raise MessageNotFoundError(
                f"Message '{command.inbound_message_id}' not found"
            )
        
        inbound_text = inbound.content.value if inbound.content else ""

        conversation = await self.create_conversation.execute(
            CreateConversationCommand(
                customer_id = inbound.customer_id,
                bot_user_id = inbound.user_id,
                source = inbound.source,
            )
        )

        if self._customer_requested_human(inbound_text):
            await self._escalate(
                conversation.id,
                inbound,
                reason = "customer_requested",
            )
            return AnalyzeMessageResult(
                outcome = AnalysisOutcome.ESCALATED_BY_REQUEST,
                inbound_message = inbound,
                conversation = conversation,
            )
        
        if not conversation.is_bot_active:
            return AnalyzeMessageResult(
                outcome = AnalysisOutcome.HUMAN_HANDLING,
                inbound_message = inbound,
                conversation = conversation,
            )
        
        history = await self.message_repo.list_by_customer(
            customer_id = inbound.customer_id,
            limit = CONVERSATION_HISTORY_SIZE,
            offset = 0,
            order_by_created_asc = True,
        )
        conversation_context = self._build_context(history, inbound)
        ai_response = await self.ai_gateway.generate_response(conversation_context)

        if ai_response.confidence < AI_CONFIDENCE_THRESHOLD:
            await self._escalate(
                conversation.id,
                inbound,
                reason = "low_confidence",
            )
            return AnalyzeMessageResult(
                outcome = AnalysisOutcome.ESCALATED_LOW_CONFIENCE,
                inbound_message = inbound,
                conversation = conversation,
            )
        
        outbound = await self.queue_outbound.execute(
            QueueOutboundMessageCommand(
                customer_id = inbound.customer_id,
                user_id = inbound.user_id,
                content = ai_response.content,
                source = inbound.source,
                automated = True,
            )
        )

        return AnalyzeMessageResult(
            outcome = AnalysisOutcome.AI_REPLIED,
            inbound_message = inbound,
            outbound_message = outbound,
            conversation = conversation,
        )
    
    async def _escalate(
        self,
        conversation_id: UUID,
        inbound: Message,
        reason: str,
    ) -> None:
        inbound.status = MessageStatus.ESCALATED
        await self.message_repo.update(inbound)
        await self.escalate_conversation.execute(
            EscalateConversationCommand(
                conversation_id = conversation_id,
                reason = reason
            )
        )
    
    def _customer_requested_human(self, text: str) -> bool:
        normalized = text.lower().strip()
        return any(trigger in normalized for trigger in HUMAN_ESCALATION_TRIGGERS)
    
    def _build_context(
        self,
        history: list[Message],
        inbound: Message,
    ) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = []

        for msg in history:
            if msg.id == inbound.id or msg.content is None:
                continue
            role = "assistant" if msg.direction == MessageDirection.OUTBOUND else "user"
            messages.append({"role": role, "content": msg.content.value})

        if inbound.content:
            messages.append({"role": "user", "content": inbound.content.value})

        return messages
