from openai import AsyncOpenAI
from domain.interfaces.ai_responder_gateway import IAIResponderGateway
from core.config import settings

class AIResponderGatewayOpenai(IAIResponderGateway):
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPEN_API_KEY)

    async def generate_response(self, message: str) -> str:
        response = await self.client.responses.create(
            model="gpt-4.1-mini",
            input=message,
            timeout=20
        )
        return response.output_text
