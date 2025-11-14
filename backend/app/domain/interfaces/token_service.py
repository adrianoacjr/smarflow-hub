from datetime import timedelta
from abc import ABC, abstractmethod

class ITokenService(ABC):
    @abstractmethod
    def create_access_token(self, subject: str, expires_in: timedelta) -> str:
        pass

    @abstractmethod
    def verify_access_token(self, token:str) -> str:
        pass
