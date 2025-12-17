from openai import AsyncOpenAI
from core.config import settings

class OpenAIClientFactory:
    @staticmethod
    def create() -> AsyncOpenAI:
        return AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            timeout=settings.OPENAI_TIMEOUT,
            max_retries=settings.OPENAI_MAX_RETRIES
        )
