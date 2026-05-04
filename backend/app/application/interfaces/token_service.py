from datetime import timedelta
from abc import ABC, abstractmethod
from typing import Optional

class ITokenService(ABC):
    @abstractmethod
    def create_access_token(
        self,
        subject: str,
        extra_claims: Optional[dict] = None,
        expires_in: Optional[timedelta] = None,
    ) -> str:
        pass

    @abstractmethod
    def verify_access_token(self, token: str) -> dict:
        pass
