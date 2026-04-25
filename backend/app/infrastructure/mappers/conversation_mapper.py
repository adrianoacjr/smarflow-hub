from uuid import UUID

from domain.entities.conversation import Conversation
from domain.enums.conversation_status import ConversationStatus
from domain.enums.message_source import MessageSource
from infrastructure.orm.conversation_orm import ConversationORM

class ConversationMapper:
    @staticmethod
    def orm_to_domain(orm: ConversationORM) -> Conversation:
        return Conversation(
            id=orm.id,
            customer_id=orm.customer_id,
            bot_user_id=orm.bot_user_id,
            assigned_agent_id=orm.assigned_agent_id,
            source=MessageSource(orm.source),
            status=ConversationStatus(orm.status),
            created_at=orm.created_at,
            updated_at=orm.updated_at,
            resolved_at=orm.resolved_at,
        )
    
    @staticmethod
    def domain_to_orm(domain: Conversation) -> ConversationORM:
        return ConversationORM(
            id=domain.id,
            customer_id=domain.customer_id,
            bot_user_id=domain.bot_user_id,
            assigned_agent_id=domain.assigned_agent_id,
            source=domain.source.value,
            status=domain.status.value,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
            resolved_at=domain.resolved_at,
        )
