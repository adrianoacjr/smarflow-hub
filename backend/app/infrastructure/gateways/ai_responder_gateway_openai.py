from openai import AsyncOpenAI, APITimeoutError, APIStatusError
from typing import Optional

from application.interfaces.ai_responder_gateway import AIResponse, IAIResponderGateway

_DEFAULT_CONFIDENCE = 1.0
_LOW_CONFIDENCE = 0.4

class AIResponderGatewayOpenai(IAIResponderGateway):
    def __init__(
        self,
        client: AsyncOpenAI,
        model: str,
        system_prompt: str,
    ) -> None:
        self._client = client
        self._model = model
        self._system_prompt = system_prompt

    async def generate_response(
        self,
        message: list[dict[str, str]],
        system_prompt_override: Optional[str] = None,
    ) -> AIResponse:
        prompt = system_prompt_override or self._system_prompt
        messages = self._with_system_prompt(message, prompt)

        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
            )
        except APITimeoutError as e:
            raise RuntimeError("AI request timed out") from e
        except APIStatusError as e:
            raise RuntimeError(f"AI provider error: {e.status_code}") from e
        
        choice = response.choices[0]
        content = choice.message.content or ""

        confidence = _DEFAULT_CONFIDENCE if choice.finish_reason == "stop" else _LOW_CONFIDENCE
        return AIResponse(content=content, confidence=confidence)
    
    def _with_system_prompt(
        self,
        messages: list[dict[str, str]],
        prompt: str,
    ) -> list[dict[str, str]]:
        if messages and messages[0].get("role") == "system":
            return messages
        return [{"role": "system", "content": prompt}, *messages]
