from domain.models.user import User
from domain.interfaces.user_repository import IUserRepository
import bcrypt
from datetime import datetime

class CreateUser:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def execute(self, name: str, email: str, password: str, access_level: str, created_at: datetime) -> User:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(id=0, name=name, email=email, password_hash=hashed_password, access_level=access_level, created_at=created_at)
        created_user = self.repo.create(new_user)
        return created_user
