from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from domain.entities.conversation import Conversation
from domain.enums.conversation_status import ConversationStatus
from domain.enums.message_source import MessageSource

class IConversationRepository(ABC):
    @abstractmethod
    async def create(self, conversation: Conversation) -> Conversation:
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, conversation: Conversation) -> Conversation:
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_active_by_customer(
        self,
        customer_id: int,
        source: MessageSource,
    ) -> Optional[Conversation]:
        raise NotImplementedError
    
    @abstractmethod
    async def list_by_status(
        self,
        status: ConversationStatus,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Conversation]:
        raise NotImplementedError
    
    @abstractmethod
    async def count_by_status(self, status: ConversationStatus) -> int:
        raise NotImplementedError
    
    @abstractmethod
    async def list_by_customer(
        self,
        customer_id: int,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Conversation]:
        raise NotImplementedError
