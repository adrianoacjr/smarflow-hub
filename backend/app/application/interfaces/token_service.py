from datetime import timedelta
from abc import ABC, abstractmethod

class ITokenService(ABC):
    @abstractmethod
    def create_access_token(
        self,
        subject: str,
        expires_in: timedelta,
        extra_claims: dict | None = None,
    ) -> str:
        pass

    @abstractmethod
    def verify_access_token(self, token: str) -> dict:
        pass
