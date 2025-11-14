from pydantic import BaseModel
from domain.models.message import Message

class MessageCreateDTO(BaseModel):
    user_id: int
    content: str
    source: str

class MessageResponseDTO(BaseModel):
    id: int
    user_id: int
    content: str
    timestamp: str
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
