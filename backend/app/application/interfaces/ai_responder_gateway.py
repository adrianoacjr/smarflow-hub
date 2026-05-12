from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True, slots=True)
class AIResponse:
    content: str
    confidence: float

class IAIResponderGateway(ABC):
    @abstractmethod
    async def generate_response(
        self,
        message: list[dict[str, str]],
        system_prompt_override: Optional[str] = None,    
    ) -> AIResponse:
        raise NotImplementedError
