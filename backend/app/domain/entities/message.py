from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from domain.enums.message_direction import MessageDirection
from domain.enums.message_source import MessageSource
from domain.enums.message_status import MessageStatus
from domain.value_objects.message_content import MessageContent

@dataclass(eq=False, slots=True, kw_only=True)
class Message:
    customer_id: int
    content: MessageContent
    direction: MessageDirection
    source: MessageSource
    created_at: datetime
    automated: bool
    status: MessageStatus
    user_id: Optional[int] = None
    id: Optional[int] = None

    def mark_as_sent(self) -> None:
        self.status = MessageStatus.SENT

    def mask_as_delivered(self) -> None:
        self.status = MessageStatus.DELIVERED

    def mark_as_failed(self) -> None:
        self.status = MessageStatus.FAILED
