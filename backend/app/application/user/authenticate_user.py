from domain.models.user import User
from domain.interfaces.user_repository import IUserRepository
from typing import Optional
import bcrypt

class AuthenticateUser:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def execute(self, email: str, password: str) -> Optional[User]:
        users = self.repo.get_all()
        user = next((u for u in users if u.email == email), None)
        if not user:
            return None
        if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash):
            return None
        return user
