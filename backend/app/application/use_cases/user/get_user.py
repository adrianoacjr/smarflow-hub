from typing import Optional

from domain.entities.user import User
from domain.interfaces.user_repository import IUserRepository

class GetUser:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def execute(self, user_id: int) -> Optional[User]:
        return self.repo.get_by_id(user_id)
