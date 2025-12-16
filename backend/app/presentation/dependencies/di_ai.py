from domain.interfaces.ai_responder_gateway import IAIResponderGateway

from application.integration.generate_ai_reply import GenerateAIReply

from infrastructure.gateways.ai_responder_gateway_openai import AIResponderGatewayOpenai

class DIAI:
    def get_ai_response_service(self) -> IAIResponderGateway:
        return GenerateAIReply()