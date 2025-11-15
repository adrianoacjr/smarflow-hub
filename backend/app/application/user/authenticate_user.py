from typing import Optional
from datetime import timedelta
import bcrypt

from domain.interfaces.user_repository import IUserRepository
from domain.interfaces.token_service import ITokenService


class AuthenticateUser:
    def __init__(self, repo: IUserRepository, token_service: ITokenService):
        self.repo = repo
        self.token_service = token_service

    def execute(self, email: str, password: str) -> Optional[str]:
        user = self.repo.get_by_email(email)
        if not user:
            return None

        if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash):
            return None

        token = self.token_service.create_access_token(
            user.email,
            expires_in=timedelta(minutes=60)
        )
        return token
