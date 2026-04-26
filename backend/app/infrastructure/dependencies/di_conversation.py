from sqlalchemy.ext.asyncio import AsyncSession

from application.use_cases.conversation.create_conversation import CreateConversation
from application.use_cases.conversation.escalate_conversation import EscalateConversation
from infrastructure.repositories.conversation_repository_postgres import ConversationRepositoryPostgres
from infrastructure.dependencies.di_customer import get_customer_repository
from infrastructure.dependencies.di_user import get_user_repository


def get_conversation_repository(session: AsyncSession) -> ConversationRepositoryPostgres:
    return ConversationRepositoryPostgres(session)


def get_create_conversation(session: AsyncSession) -> CreateConversation:
    return CreateConversation(
        conversation_repo=get_conversation_repository(session),
        customer_repo=get_customer_repository(session),
        user_repo=get_user_repository(session),
    )


def get_escalate_conversation(session: AsyncSession) -> EscalateConversation:
    return EscalateConversation(
        conversation_repo=get_conversation_repository(session),
    )
