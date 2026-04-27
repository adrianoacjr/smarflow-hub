from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID

from domain.enums.message_direction import MessageDirection
from domain.enums.message_source import MessageSource
from domain.enums.message_status import MessageStatus
from domain.value_objects.message_content import MessageContent

@dataclass(eq=False, slots=True, kw_only=True)
class MessageAttachment:
    url: str
    mime_type: str
    filename: str | None = None

@dataclass(eq=False, slots=True, kw_only=True)
class Message:
    id: UUID
    customer_id: int
    user_id: int
    content: MessageContent | None
    direction: MessageDirection
    source: MessageSource
    created_at: datetime
    automated: bool
    status: MessageStatus
    attachments: tuple[MessageAttachment, ...] = field(default_factory=tuple)
    conversation_id: Optional[UUID] = None

    def __post_init__(self) -> None:
        if self.content is None and not self.attachments:
            raise ValueError("message must have content or attachments")

    def mark_as_sent(self) -> None:
        if self.direction != MessageDirection.OUTBOUND:
            raise ValueError("only outbound messages can be marked as sent")
        if self.status != MessageStatus.PENDING:
            raise ValueError("only pending messages can be marked as sent")
        self.status = MessageStatus.SENT

    def mark_as_delivered(self) -> None:
        if self.status != MessageStatus.SENT:
            raise ValueError("only sent messages can be marked as delivered")
        self.status = MessageStatus.DELIVERED

    def mark_as_failed(self) -> None:
        if self.direction != MessageDirection.OUTBOUND:
            raise ValueError("only outbound messages can be marked as failed")
        self.status = MessageStatus.FAILED

    def update_status(self, new_status: MessageStatus) -> None:
        valid_transitions = {
            MessageStatus.PENDING: {MessageStatus.SENT, MessageStatus.FAILED},
            MessageStatus.SENT: {MessageStatus.DELIVERED, MessageStatus.FAILED},
            MessageStatus.RECEIVED: set(),
            MessageStatus.DELIVERED: set(),
            MessageStatus.FAILED: set(),
        }

        allowed = valid_transitions.get(self.status, set())
        if new_status not in allowed:
            raise ValueError(f"Invalid status transition: {self.status}) -> {new_status}")
        
        self.status = new_status

