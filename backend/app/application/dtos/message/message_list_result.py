from dataclasses import dataclass

from domain.entities.message import Message

@dataclass(frozen=True, slots=True)
class MessageListResult:
    items: tuple[Message, ...]
    total: int
    limit: int
    offset: int
