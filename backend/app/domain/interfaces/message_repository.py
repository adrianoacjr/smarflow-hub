from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.message import Message

class IMessageRepository(ABC):
    @abstractmethod
    async def create(self, message: Message) -> Message:
        raise NotImplementedError
    
    async def update(self, message: Message) -> Message:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, message_id: int) -> Optional[Message]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_user(self, user_id: int, limit: int = 50, offset: int = 0) -> list[Message]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_customer(self, customer_id: int, limit: int = 50, offset: int = 0) -> list[Message]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, message_id: int) -> bool:
        pass
