from domain.models.message import Message
from abc import ABC, abstractmethod

class IMessageRepository(ABC):
    @abstractmethod
    def send_message(self, message: Message) -> Message:
        pass

    @abstractmethod
    def get_message_by_id(self, message_id: int) -> Message:
        pass

    @abstractmethod
    def get_all_messages(self) -> list[Message]:
        pass

    @abstractmethod
    def delete_message(self, message_id: int) -> None:
        pass
