from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.customer import Customer
from domain.enums.message_source import MessageSource
from domain.value_objects.email_address import EmailAddress
from domain.value_objects.phone_number import PhoneNumber

class ICustomerRepository(ABC):
    @abstractmethod
    async def create(self, customer: Customer) -> Customer:
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, customer: Customer) -> Customer:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, customer_id: int) -> Optional[Customer]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: EmailAddress) -> Optional[Customer]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_phone(self, phone: PhoneNumber) -> Optional[Customer]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_source_ref(
        self,
        source: MessageSource,
        source_customer_ref: str,
    ) -> Optional[Customer]:
        raise NotImplementedError
    
    @abstractmethod
    async def create_placeholder(
        self,
        source: MessageSource,
        source_customer_ref: str,
        name: str | None = None,
    ) -> Customer:
        raise NotImplementedError

    @abstractmethod
    async def list(self, limit: int = 50, offset: int = 0) -> list[Customer]:
        raise NotImplementedError
