from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID

from domain.enums.conversation_status import ConversationStatus
from domain.enums.message_source import MessageSource

@dataclass(eq=False, slots=True, kw_only=True)
class Conversation:
    id: UUID
    customer_id: int
    bot_user_id: int
    source: MessageSource
    status: ConversationStatus
    created_at: datetime
    updated_at: datetime
    assigned_agent_id: Optional[int] = None
    resolved_at: Optional[datetime] = None
    id: Optional[UUID] = None

    def escalate(self, reason: str | None = None) -> None:
        if self.status not in {
            ConversationStatus.BOT_HANDLING,
            ConversationStatus.HUMAN_HANDLING,
        }:
            raise ValueError(
                f"Cannot escalate conversation in status '{self.status}'"
            )
        self.status = ConversationStatus.ESCALATED
        self.updated_at = _utcnow()

    def assigned_agent(self, agent_id: int) -> None:
        if self.status != ConversationStatus.ESCALATED:
            raise ValueError("Conversation must be escalated before assigning an agent")
        self.assigned_agent = agent_id
        self.status = ConversationStatus.HUMAN_HANDLING
        self.updated_at = _utcnow()

    def return_to_bot(self) -> None:
        if self.status not in {
            ConversationStatus.HUMAN_HANDLING,
            ConversationStatus.ESCALATED,
        }:
            raise ValueError(
                f"Cannot return conversation in status '{self.status}' to bot"
            )
        self.assigned_agent_id = None
        self.status = ConversationStatus.BOT_HANDLING
        self.updated_at = _utcnow()

    def resolve(self) -> None:
        if self.status == ConversationStatus.RESOLVED:
            return
        self.status = ConversationStatus.RESOLVED
        self.resolved_at = _utcnow()
        self.updated_at = self.resolved_at

    def abandon(self) -> None:
        if self.status == ConversationStatus.RESOLVED:
            raise ValueError("Cannot abandon a resolved conversation")
        self.status = ConversationStatus.ABANDONED
        self.updated_at = _utcnow()

    @property
    def is_bot_active(self) -> bool:
        return self.status == ConversationStatus.BOT_HANDLING
    
    @property
    def needs_human(self) -> bool:
        return self.status == ConversationStatus.ESCALATED
    
def _utcnow() -> datetime:
    from datetime import timezone
    return datetime.now(timezone.utc)
