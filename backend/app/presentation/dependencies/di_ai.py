from openai import AsyncOpenAI

from domain.interfaces.ai_responder_gateway import IAIResponderGateway

from application.integration.generate_ai_reply import GenerateAIReply

from infrastructure.gateways.ai_responder_gateway_openai import AIResponderGatewayOpenai

class DIAI:
    def get_ai_gateway(self, client: AsyncOpenAI) -> IAIResponderGateway:
        return AIResponderGatewayOpenai(client)

    def get_generate_ai_reply_service(self, client: AsyncOpenAI) -> GenerateAIReply:
        return GenerateAIReply(self.get_ai_gateway(client))
    
di_ai = DIAI()
