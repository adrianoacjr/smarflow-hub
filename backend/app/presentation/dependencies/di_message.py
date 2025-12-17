from sqlalchemy.ext.asyncio import AsyncSession

from domain.interfaces.message_repository import IMessageRepository

from application.integration.receive_whatsapp_message import ReceiveWhatsAppMessage

from infrastructure.repositories.message_repository_postgres import MessageRepositoryPostgres

class DIMessage:
    def get_message_repository(self, session: AsyncSession) -> IMessageRepository:
        return MessageRepositoryPostgres(session)

    def get_receive_whatsapp_message(self, session: AsyncSession) -> ReceiveWhatsAppMessage:
        return ReceiveWhatsAppMessage(self.get_message_repository(session))
    
di_message = DIMessage()
