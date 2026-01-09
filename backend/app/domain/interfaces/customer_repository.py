from abc import ABC, abstractmethod
from typing import Optional, List

from domain.entities.customer import Customer

class ICustomerRepository(ABC):
    @abstractmethod
    def create(self, user: Customer) -> Customer:
        pass

    @abstractmethod
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Customer]:
        pass

    @abstractmethod
    def get_by_phone_number(self, phone: str) -> Optional[Customer]:
        pass

    @abstractmethod
    def get_all(self, limit: int = 50, offset: int = 0) -> List[Customer]:
        pass

    @abstractmethod
    def delete(self, customer_id: int) -> None:
        pass
