from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.user import User
from domain.value_objects.email_address import EmailAddress

class IUserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: EmailAddress) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def list(self, limit: int = 50, offset: int = 0) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        raise NotImplementedError
