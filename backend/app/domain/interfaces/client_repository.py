from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.client import Client
from domain.value_objects.email_address import EmailAddress

class IClientRepository(ABC):
    @abstractmethod
    async def create(self, client: Client) -> Client:
        raise NotImplementedError
    
    @abstractmethod
    async def update( self, client: Client) -> Client:
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, client: int) -> Optional[Client]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_email(self, email: EmailAddress) -> Optional[Client]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_api_key_hash(self, api_key_hash: str) -> Optional[Client]:
        raise NotImplementedError
    
    @abstractmethod
    async def list(self, limit: int = 50, offset: int = 0) -> list[Client]:
        raise NotImplementedError
    
    @abstractmethod
    async def count(self) -> int:
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, client_if: int) -> bool:
        raise NotImplementedError
