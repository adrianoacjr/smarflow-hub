from domain.models.message import Message
from domain.interfaces.message_repository import IMessageRepository
from datetime import datetime, timezone

class SendMessage:
    def __init__(self, message_repository: IMessageRepository):
        self.repo = message_repository

    def execute(self, user_id: int, content: str, source: str) -> Message:
        new_message = Message(user_id=user_id, timestamp=datetime.now(timezone.utc), content=content, source=source)
        sent_message = self.repo.send_message(new_message)
        return sent_message

