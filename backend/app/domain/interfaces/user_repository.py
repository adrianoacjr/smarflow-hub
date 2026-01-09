from abc import ABC, abstractmethod
from typing import Optional, List

from domain.entities.user import User

class IUserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_all(self, limit: int = 50, offset: int = 0) -> List[User]:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass
