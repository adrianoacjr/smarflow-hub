from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from domain.enums.conversation_status import ConversationStatus
from domain.enums.message_source import MessageSource
from domain.utils.time import utcnow

@dataclass(eq=False, slots=True, kw_only=True)
class Conversation:
    client_id: UUID
    user_id: UUID
    customer_id: UUID
    bot_user_id: UUID
    source: MessageSource
    status: ConversationStatus
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)
    resolved_at: Optional[datetime] = None
    id: Optional[UUID] = field(default_factory=uuid4)

    def escalate(self, reason: str | None = None) -> None:
        if self.status not in {
            ConversationStatus.BOT_HANDLING,
            ConversationStatus.HUMAN_HANDLING,
        }:
            raise ValueError(
                f"Cannot escalate conversation in status '{self.status}'"
            )
        self.status = ConversationStatus.ESCALATED
        self.updated_at = utcnow()

    def assign_agent(self, agent_id: UUID) -> None:
        if self.status != ConversationStatus.ESCALATED:
            raise ValueError("Conversation must be escalated before assigning an agent")
        self.user_id = agent_id
        self.status = ConversationStatus.HUMAN_HANDLING
        self.updated_at = utcnow()

    def return_to_bot(self) -> None:
        if self.status not in {
            ConversationStatus.HUMAN_HANDLING,
            ConversationStatus.ESCALATED,
        }:
            raise ValueError(
                f"Cannot return conversation in status '{self.status}' to bot"
            )
        self.user_id = self.bot_user_id
        self.status = ConversationStatus.BOT_HANDLING
        self.updated_at = utcnow()

    def resolve(self) -> None:
        if self.status == ConversationStatus.RESOLVED:
            return
        self.status = ConversationStatus.RESOLVED
        self.resolved_at = utcnow()
        self.updated_at = self.resolved_at

    def abandon(self) -> None:
        if self.status == ConversationStatus.RESOLVED:
            raise ValueError("Cannot abandon a resolved conversation")
        self.status = ConversationStatus.ABANDONED
        self.updated_at = utcnow()

    @property
    def is_bot_active(self) -> bool:
        return self.status == ConversationStatus.BOT_HANDLING
    
    @property
    def needs_human(self) -> bool:
        return self.status == ConversationStatus.ESCALATED
