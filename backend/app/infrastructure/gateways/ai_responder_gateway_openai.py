import asyncio
from openai import OpenAIError

from domain.interfaces.ai_responder_gateway import IAIResponderGateway

class AIResponderGatewayOpenai(IAIResponderGateway):
    def __init__(self, client):
        self.client = client

    async def generate_response(self, message: str) -> str:
        try:
            response = await self.client.responses.create(
                model="gpt-4.1-mini",
                input=message,
                timeout=20
            )
            return response.output_text
        except OpenAIError as e:
            raise RuntimeError("AI provider error") from e
        
        except asyncio.TimeoutError:
            raise RuntimeError("AI request timeout")
