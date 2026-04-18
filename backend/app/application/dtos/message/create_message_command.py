from dataclasses import dataclass

from domain.enums.message_direction import MessageDirection
from domain.enums.message_source import MessageSource

@dataclass(frozen=True, slots=True)
class CreateMessageCommand:
    customer_id: int
    user_id: int
    content: str
    direction: MessageDirection
    source: MessageSource
    automated: bool
