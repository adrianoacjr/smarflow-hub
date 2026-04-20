from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class AIResponse:
    content: str
    confidence: float

class IAIResponderGateway(ABC):
    @abstractmethod
    async def generate_response(self, message: list[dict[str, str]],) -> AIResponse:
        raise NotImplementedError
