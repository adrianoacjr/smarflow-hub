from dataclasses import dataclass

from domain.enums.message_direction import MessageDirection
from domain.enums.message_source import MessageSource
from domain.enums.message_status import MessageStatus

@dataclass(frozen=True, slots=True)
class CreateMessageCommand:
    customer_id: int
    content: str
    direction: MessageDirection
    source: MessageSource
    automated: bool
    status: MessageStatus
    user_id: int | None = None
