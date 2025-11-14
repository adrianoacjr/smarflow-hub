"""
Use case for authenticating a user based on email and password.
Generates an access token upon successful authentication.
"""

from typing import Optional
from datetime import timedelta
import bcrypt

from domain.interfaces.user_repository import IUserRepository
from domain.interfaces.token_service import ITokenService


class AuthenticateUser:
    """
    Handles the authentication logic for validating user credentials
    and generating an access token using the configured token service.
    """

    def __init__(self, repo: IUserRepository, token_service: ITokenService):
        """
        Initialize the AuthenticateUser use case.

        Args:
            repo (IUserRepository): Repository abstraction for accessing user data.
            token_service (ITokenService): Service responsible for generating tokens.
        """
        self.repo = repo
        self.token_service = token_service

    def execute(self, email: str, password: str) -> Optional[str]:
        """
        Authenticate a user using email and password.

        Args:
            email (str): User's email.
            password (str): Plain text password.

        Returns:
            Optional[str]: A JWT access token if authentication succeeds,
                           otherwise None.
        """
        user = self.repo.get_by_email(email)
        if not user:
            return None

        if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            return None

        token = self.token_service.create_access_token(
            user.email,
            expires_in=timedelta(minutes=60)
        )
        return token
