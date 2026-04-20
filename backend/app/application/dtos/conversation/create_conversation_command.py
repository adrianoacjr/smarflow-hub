from dataclasses import dataclass

from domain.enums.message_source import MessageSource

@dataclass(frozen=True, slots=True)
class CreateConversationCommand:
    customer_id: int
    bot_user_id: int
    source: MessageSource
