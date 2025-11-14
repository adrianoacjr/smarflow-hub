from domain.models.user import User
from domain.interfaces.user_repository import IUserRepository
from typing import Optional, List


class UserRepositoryFake(IUserRepository):
    def __init__(self):
        self._users: List[User] = []

    def create(self, user: User) -> User:
        if len(self._users) == 0:
            user.id = 1
        else:
            user.id = max(user.id for user in self._users) + 1
        self._users.append(user)
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        return next((user for user in self._users if user.id == user_id), None)
    
    def get_all(self) -> List[User]:
        return self._users

    def delete(self, user_id: int) -> None:
        self._users = [user for user in self._users if user.id != user_id]

    def get_by_email(self, email: str):
        return next((user for user in self._users if user.email == email), None)
