from domain.entities.message import Message
from abc import ABC, abstractmethod
from typing import Optional, List

class IMessageRepository(ABC):
    @abstractmethod
    def create(self, message: Message) -> Message:
        pass

    @abstractmethod
    def get_by_id(self, message_id: int) -> Optional[Message]:
        pass

    @abstractmethod
    def list_by_user(self, user_id: int, limit: int = 50, offset: int = 0) -> List[Message]:
        pass

    @abstractmethod
    def list_by_customer(self, customer_id: int, limit: int = 50, offset: int = 0) -> List[Message]:
        pass

    @abstractmethod
    def delete(self, message_id: int) -> None:
        pass
