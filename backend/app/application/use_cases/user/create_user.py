from datetime import datetime

import bcrypt

from domain.entities.user import User
from domain.interfaces.user_repository import IUserRepository

class CreateUser:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(self, name: str, email: str, password: str, access_level: str, created_at: datetime) -> User:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        password_hash = hashed_password.decode("utf-8")
        new_user = User(
            name=name,
            email=email,
            password_hash=password_hash,
            access_level=access_level,
            created_at=created_at
        )
        return await self.repo.create(new_user)
