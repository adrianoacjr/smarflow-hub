from typing import List

from domain.entities.user import User
from domain.interfaces.user_repository import IUserRepository

class GetAllUsers:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def execute(self) -> List[User]:
        return self.repo.get_all()
