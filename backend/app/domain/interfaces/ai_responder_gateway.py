from abc import ABC, abstractmethod

class IAIResponderGateway(ABC):
    @abstractmethod
    async def generate_response(self, message: str) -> str:
        pass
