from sqlalchemy.ext.asyncio import AsyncSession

from application.use_cases.message.create_message import CreateMessage
from application.use_cases.message.delete_message import DeleteMessage
from application.use_cases.message.get_message_by_id import GetMessageById
from application.use_cases.message.list_message_by_customer import ListMessageByCustomer
from application.use_cases.message.list_message_by_user import ListMessageByUser
from application.use_cases.message.queue_outbound_message import QueueOutboundMessage
from application.use_cases.message.analyze_message import AnalyzeMessage
from application.use_cases.message.receive_message import ReceiveMessage
from infrastructure.repositories.message_repository_postgres import MessageRepositoryPostgres
from infrastructure.dependencies.di_customer import (
    get_customer_repository,
    get_get_or_create_customer,
)
from infrastructure.dependencies.di_user import get_user_repository
from infrastructure.dependencies.di_conversation import (
    get_create_conversation,
    get_escalate_conversation,
)

def get_message_repository(session: AsyncSession) -> MessageRepositoryPostgres:
    return MessageRepositoryPostgres(session)


def get_create_message(session: AsyncSession) -> CreateMessage:
    return CreateMessage(
        message_repo=get_message_repository(session),
        customer_repo=get_customer_repository(session),
        user_repo=get_user_repository(session),
    )

def get_get_message_by_id(session: AsyncSession) -> GetMessageById:
    return GetMessageById(message_repo=get_message_repository(session))


def get_list_messages_by_user(session: AsyncSession) -> ListMessageByUser:
    return ListMessageByUser(
        message_repo=get_message_repository(session),
        user_repo=get_user_repository(session),
    )

def get_list_messages_by_customer(session: AsyncSession) -> ListMessageByCustomer:
    return ListMessageByCustomer(
        message_repo=get_message_repository(session),
        customer_repo=get_customer_repository(session),
    )

def get_queue_outbound_message(session: AsyncSession) -> QueueOutboundMessage:
    return QueueOutboundMessage(
        message_repo=get_message_repository(session),
        customer_repo=get_customer_repository(session),
        user_repo=get_user_repository(session),
    )

def get_received_message(session: AsyncSession) -> ReceiveMessage:
    return ReceiveMessage(
        message_repo=get_message_repository(session),
        user_repo=get_user_repository(session),
        get_or_create_customer=get_get_or_create_customer(session),
    )

def get_delete_message(session: AsyncSession) -> DeleteMessage:
    return DeleteMessage(message_repo=get_message_repository(session))
