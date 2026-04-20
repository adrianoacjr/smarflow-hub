from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from domain.entities.message import Message

class IMessageRepository(ABC):
    @abstractmethod
    async def create(self, message: Message) -> Message:
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, message: Message) -> Message:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, message_id: UUID) -> Optional[Message]:
        raise NotImplementedError
    
    @abstractmethod
    async def list_by_customer(
        self,
        customer_id: int,
        limit: int = 50,
        offset: int = 0,
        order_by_created_asc: bool = True,
    ) -> list[Message]:
        raise NotImplementedError
    
    @abstractmethod
    async def count_by_customer(self, customer_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    async def list_by_user(self, user_id: int, limit: int = 50, offset: int = 0) -> list[Message]:
        raise NotImplementedError
    
    @abstractmethod
    async def count_by_user(self, user_id: int) -> int:
        raise NotImplementedError
    
    @abstractmethod
    async def list_by_conversation(
        self,
        conversation_id: UUID,
        limit: int = 50,
        offset: int = 0,
        order_by_created_asc: bool = True,
    ) -> list[Message]:
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, message_id: UUID) -> bool:
        raise NotImplementedError
