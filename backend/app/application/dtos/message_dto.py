from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field

from domain.entities.message import Message

class MessageCreateDTO(BaseModel):
    user_id: int
    customer_id: int
    content: str = Field(..., max_length=4096)
    direction: str = Field(..., pattern="^(inbound|outbound)$")
    source: str = Field(..., pattern="^(whatsapp|instagram|other)$")
    created_at: datetime
    automated: bool
    status: str = Field(..., pattern="^(created|queued|sending|received|sent|delivered|read|failed|rejected|expired|blocked|deleted|unsupported)$")

class MessageResponseDTO(BaseModel):
    id: int
    user_id: int
    customer_id: int
    content: str
    direction: str
    source: str
    created_at: datetime
    automated: bool
    source: str

    @staticmethod
    def from_domain(message: Message):
        return MessageResponseDTO(
            id=message.id,
            user_id=message.user_id,
            content=message.content,
            timestamp=message.timestamp.isoformat(),
            source=message.source
        )
