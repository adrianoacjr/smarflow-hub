from sqlalchemy.ext.asyncio import AsyncSession

from domain.interfaces.message_repository import IMessageRepository

from application.interfaces.ai_responder_gateway import IAIResponderGateway
from application.use_cases.integration.generate_ai_reply import GenerateAIReply
from application.use_cases.message.save_outbound_message import SaveOutboundMessage
from application.use_cases.integration.process_ai_reply import ProcessAIReply

from adapters.gateways.ai_responder_gateway_openai import AIResponderGatewayOpenai
from adapters.gateways.openai_client import OpenAIClientFactory
from adapters.repositories.message_repository_postgres import MessageRepositoryPostgres

class DIAI:
    def get_message_repository(self, session: AsyncSession) -> IMessageRepository:
        return MessageRepositoryPostgres(session)

    def get_ai_gateway(self) -> IAIResponderGateway:
        client = OpenAIClientFactory.create()
        return AIResponderGatewayOpenai(client)

    def get_generate_ai_reply_service(self) -> GenerateAIReply:
        return GenerateAIReply(self.get_ai_gateway())
        
    def get_save_outbound_message_service(self, session: AsyncSession) -> SaveOutboundMessage:
        return SaveOutboundMessage(self.get_message_repository(session))

    def get_process_ai_reply_service(self, session: AsyncSession) -> ProcessAIReply:
        return ProcessAIReply(
            self.get_generate_ai_reply_service(),
            self.get_save_outbound_message_service(session)
        )

di_ai = DIAI()
