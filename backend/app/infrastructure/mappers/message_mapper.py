from domain.entities.message import Message
from domain.enums.message_direction import MessageDirection
from domain.enums.message_source import MessageSource
from domain.enums.message_status import MessageStatus
from domain.value_objects.message_content import MessageContent
from infrastructure.orm.message_orm import MessageORM

class MessageMapper:
    @staticmethod
    def orm_to_domain(orm: MessageORM) -> Message:
        return Message(
            id=orm.id,
            user_id=orm.user_id,
            customer_id=orm.customer_id,
            conversation_id=orm.conversation_id,
            content=MessageContent(orm.content) if orm.content else None,
            direction=MessageDirection(orm.direction),
            source=MessageSource(orm.source),
            created_at=orm.created_at,
            automated=orm.automated,
            status=MessageStatus(orm.status),
            attachments=tuple(),
        )
    
    @staticmethod
    def domain_to_orm(domain: Message) -> MessageORM:
        return MessageORM(
            id=domain.id,
            user_id=domain.user_id,
            customer_id=domain.customer_id,
            conversation_id=domain.conversation_id,
            content=domain.content.value if domain.content else None,
            direction=domain.direction.value,
            source=domain.source.value,
            created_at=domain.created_at,
            automated=domain.automated,
            status=domain.status.value,
        )
