from domain.interfaces.ai_responder_gateway import IAIResponderGateway

from application.integration.generate_ai_reply import GenerateAIReply

from infrastructure.gateways.ai_responder_gateway_openai import AIResponderGatewayOpenai
from infrastructure.gateways.openai_client import OpenAIClientFactory

class DIAI:
    def get_ai_gateway(self) -> IAIResponderGateway:
        client = OpenAIClientFactory.create()
        return AIResponderGatewayOpenai(client)

    def get_generate_ai_reply_service(self) -> GenerateAIReply:
        return GenerateAIReply(self.get_ai_gateway())
    
di_ai = DIAI()
