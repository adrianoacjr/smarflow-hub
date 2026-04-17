from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.customer import Customer
from domain.value_objects.email_address import EmailAddress
from domain.value_objects.phone_number import PhoneNumber

class ICustomerRepository(ABC):
    @abstractmethod
    def create(self, customer: Customer) -> Customer:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, customer: Customer) -> Customer:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: EmailAddress) -> Optional[Customer]:
        raise NotImplementedError

    @abstractmethod
    def get_by_phone(self, phone: PhoneNumber) -> Optional[Customer]:
        raise NotImplementedError

    @abstractmethod
    def list(self, limit: int = 50, offset: int = 0) -> list[Customer]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, customer_id: int) -> bool:
        raise NotImplementedError
