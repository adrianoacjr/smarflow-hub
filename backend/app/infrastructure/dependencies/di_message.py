from sqlalchemy.ext.asyncio import AsyncSession

from application.use_cases.integration.receive_whatsapp_message import ReceiveWhatsAppMessage
from application.use_cases.message.create_message import CreateMessage
from application.use_cases.message.get_message_by_id import GetMessageById
from application.use_cases.message.list_message_by_user import ListMessageByUser
from application.use_cases.message.list_message_by_customer import ListMessageByCustomer
from application.use_cases.message.delete_message import DeleteMessage

from infrastructure.repositories.message_repository_postgres import MessageRepositoryPostgres

class DIMessage:
    def build(
        self,
        session: AsyncSession,
    ) -> tuple[
        ReceiveWhatsAppMessage,
        CreateMessage,
        GetMessageById,
        ListMessageByUser,
        ListMessageByCustomer,
        DeleteMessage,
    ]:
        repo = MessageRepositoryPostgres(session)

        return (
            ReceiveWhatsAppMessage(repo),
            CreateMessage(repo),
            GetMessageById(repo),
            ListMessageByUser(repo),
            ListMessageByCustomer(repo),
            DeleteMessage(repo),
        )
    # def get_message_repository(self, session: AsyncSession) -> IMessageRepository:
    #     return MessageRepositoryPostgres(session)

    # def get_receive_whatsapp_message(self, session: AsyncSession) -> ReceiveWhatsAppMessage:
    #     return ReceiveWhatsAppMessage(self.get_message_repository(session))
    
di_message = DIMessage()
