from abc import ABC, abstractmethod

class IPasswordHasher(ABC):
    @classmethod
    @abstractmethod
    def hash(self, plain_text: str) -> str:
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def verify(self, plain_text: str, hashed_text: str) -> bool:
        raise NotImplementedError
