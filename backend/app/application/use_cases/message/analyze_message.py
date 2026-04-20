from uuid import uuid4
from datetime import datetime, timezone

from domain.constants.conversation import (
    AI_CONFIDENCE_THRESHOLD,
    CONVERSATION_HISTORY_SIZE,
    HUMAN_ESCALATION_TRIGGERS
)
from domain.entities.message import Message
from domain.enums.message_direction import MessageDirection
from domain.interfaces.message_repository import IMessageRepository
from application.dtos.message.analyze_message_command import AnalyzeMessageCommand
from application.dtos.message.analyze_message_result import AnalyzeMessageResult, AnalysisOutcome
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
    ) -> None:
        self.message_repo = message_repo
        self.ai_gateway = ai_gateway
        self.queue_outbound = queue_outbound

    async def execute(self, command: AnalyzeMessageCommand) -> AnalyzeMessageResult:
        inbound = await self.message_repo.get_by_id(command.inbound_message_id)
        if inbound is None:
            raise MessageNotFoundError(
                f"Message '{command.inbound_message_id}' not found"
            )
        
        inbound_text = inbound.content.value if inbound.content else ""

        if self._customer_requested_human(inbound_text):
            return AnalyzeMessageResult(
                outcome = AnalysisOutcome.ESCALATED_BY_REQUEST,
                inbound_message = inbound,
                outbound_message = None,
            )
        
        history = await self.message_repo.list_by_customer(
            customer_id = inbound.customer.id,
            limit = CONVERSATION_HISTORY_SIZE,
            offset = 0
        )
        conversation = self._build_conversation_context(history, inbound)

        ai_response = await self.ai_gateway.generate_response(conversation)

        if ai_response.confidence < AI_CONFIDENCE_THRESHOLD:
            return AnalyzeMessageResult(
                outcome = AnalysisOutcome.ESCALATED_LOW_CONFIENCE,
                inbound_message = inbound,
                outbound_message = None,
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
        )
    
    def _customer_requested_human(self, text: str) -> bool:
        normalized = text.lower().strip()
        return any(trigger in normalized for trigger in HUMAN_ESCALATION_TRIGGERS)
    
    def _build_conversation_context(
        self,
        history: list[Message],
        inbound: Message,
    ) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = []

        sorted_history = sorted(history, key=lambda m: m.created_at)

        for msg in sorted_history:
            if msg.id == inbound.id:
                continue
            if msg.content is None:
                continue
            role = "assistant" if msg.direction == MessageDirection.OUTBOUND else "user"
            messages.append({"role": role, "content": msg.content.value})

        if inbound.content:
            messages.append({"role": "user", "content": inbound.content.value})

        return messages
