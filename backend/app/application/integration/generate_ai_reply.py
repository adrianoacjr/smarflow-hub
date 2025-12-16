from domain.interfaces.ai_responder_gateway import IAIResponderGateway

class GenerateAIReply:
    def __init__(self, responder_service: IAIResponderGateway):
        self.responder = responder_service

    async def generate_reply(self, message: str) -> str:
        if not message.strip():
            raise ValueError("Empty message")
        
        return await self.responder.generate_response(message)
