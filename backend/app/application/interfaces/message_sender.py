from abc import ABC, abstractmethod

from domain.entities.message import Message

class IMessageSender(ABC):
    @classmethod
    @abstractmethod
    async def send(self, message: Message) -> None:
        raise NotImplementedError
