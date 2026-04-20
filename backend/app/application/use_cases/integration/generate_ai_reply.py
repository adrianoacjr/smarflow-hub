from application.interfaces.ai_responder_gateway import AIResponse, IAIResponderGateway

class GenerateAIReply:
    def __init__(self, responder: IAIResponderGateway) -> None:
        self.responder = responder

    async def execute(self, messages: list[dict[str, str]]) -> AIResponse:
        if not messages:
            raise ValueError("Message history cannot be empty")
        return await self.responder.generate_response(messages)
