from abc import ABC, abstractmethod

class IUserContext(ABC):
    @property
    @abstractmethod
    def user_id(self) -> int | None:
        raise NotImplementedError
