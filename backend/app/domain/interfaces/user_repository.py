from domain.models.user import User
from abc import ABC, abstractmethod
from typing import Optional, List

class IUserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def list(self) -> List[User]:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass
