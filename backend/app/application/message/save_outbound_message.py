from datetime import datetime, timezone

from domain.models.message import Message
from domain.interfaces.message_repository import IMessageRepository

class SaveOutboundMessage:
    def __init__(self, repo: IMessageRepository):
        self.repo = repo

    async def execute(
            self,
            *,
            customer_id: int,
            content: str,
            source: str = "ai",
            automated: bool = True,
            status: str = "sent",
    ) -> Message:
        if not content.strip():
            raise ValueError("Oubound message connot be empty")
        
        message = Message(
            customer_id=customer_id,
            content=content,
            direction="outbound",
            source=source,
            created_at=datetime.now(timezone.utc),
            automated=automated,
            status=status
        )

        return await self.repo.create(message)
