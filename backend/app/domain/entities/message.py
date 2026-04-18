from dataclasses import dataclass, field
from datetime import datetime
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

    def __post_init__(self) -> None:
        if self.content is None and not self.attachments:
            raise ValueError("message must have content or attachments")

    def mark_as_sent(self) -> None:
        self.status = MessageStatus.SENT

    def mark_as_delivered(self) -> None:
        self.status = MessageStatus.DELIVERED

    def mark_as_failed(self) -> None:
        self.status = MessageStatus.FAILED
