from domain.models.user import User
from domain.interfaces.user_repository import IUserRepository
from typing import List

class GetAllUsers:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def execute(self) -> List[User]:
        return self.repo.get_all()
