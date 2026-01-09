from typing import Optional, List

from domain.models.message import Message
from domain.interfaces.message_repository import IMessageRepository

class MessageRepositoryFake(IMessageRepository):
    def __init__(self):
        self._messages: List[Message] = []

    def send_message(self, message: Message) -> Message:
        if len(self._messages) == 0:
            message.id = 1
        else:
            message.id = max(msg.id for msg in self._messages) + 1
        self._messages.append(message)
        return message

    def get_message_by_id(self, message_id: int) -> Optional[Message]:
        return next((msg for msg in self._messages if msg.id == message_id), None)

    def get_all_messages(self) -> List[Message]:
        return self._messages

    def delete_message(self, message_id: int) -> None:
        self._messages = [msg for msg in self._messages if msg.id != message_id]

