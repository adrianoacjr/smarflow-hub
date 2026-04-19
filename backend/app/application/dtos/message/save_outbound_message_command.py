from dataclasses import dataclass

from domain.enums.message_source import MessageSource

@dataclass(frozen=True, slots=True)
class SaveOutboundMessageCommand:
    customer_id: int
    user_id: int
    content: str
    source: MessageSource
    automated: bool = True
