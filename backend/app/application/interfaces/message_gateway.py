from abc import ABC, abstractmethod

class IMessageGateway(ABC):
    @abstractmethod
    async def send_message(self, to: str, content: str) -> None:
        pass
