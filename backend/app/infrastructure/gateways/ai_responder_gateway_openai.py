import asyncio

from openai import OpenAIError

from application.interfaces.ai_responder_gateway import AIResponse, IAIResponderGateway

_DEFAULT_CONFIDENCE = 1.0

class AIResponderGatewayOpenai(IAIResponderGateway):
    def __init__(self, client) -> None:
        self.client = client

    async def generate_response(
        self,
        message: list[dict[str, str]],
    ) -> AIResponse:
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=message,
            )
            content = response.choices[0].message.content or ""
            return AIResponse(content=content, confidence=_DEFAULT_CONFIDENCE)
        
        except OpenAIError as e:
            raise RuntimeError("AI provider error") from e
        
        except asyncio.TimeoutError:
            raise RuntimeError("AI request timeout")
