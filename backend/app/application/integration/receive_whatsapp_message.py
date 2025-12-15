from datetime import datetime, timezone

from domain.models.message import Message
from domain.interfaces.message_repository import IMessageRepository

class ReceiveWhatsAppMessage:
    def __init__(self, message_repo: IMessageRepository):
        self.message_repo = message_repo

    async def execute(self, user_id: int, customer_id: int, content: str) -> Message:
        message = Message(
            user_id=user_id,
            customer_id=customer_id,
            content=content,
            direction="inbound",
            source="whatsapp",
            created_at=datetime.now(timezone.utc),
            automated=False,
            status="received"
        )

        return await self.message_repo.save(message)
