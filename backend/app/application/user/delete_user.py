from domain.models.user import User
from domain.interfaces.user_repository import IUserRepository

class DeleteUser:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def execute(self, user_id: int) -> None:
        self.repo.delete(user_id)
