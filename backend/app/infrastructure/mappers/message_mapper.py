from domain.entities.message import Message
from infrastructure.orm.message_orm import MessageORM

class MessageMapper:
    @staticmethod
    def orm_to_domain(orm: MessageORM) -> Message:
        return Message(
            id=orm.id,
            user_id=orm.user_id,
            customer_id=orm.customer_id,
            content=orm.content,
            direction=orm.direction,
            source=orm.source,
            created_at=orm.created_at,
            automated=orm.automated,
            status=orm.status
        )
    
    @staticmethod
    def domain_to_orm(domain: Message) -> MessageORM:
        orm = MessageORM(
            id=domain.id,
            user_id=domain.user_id,
            customer_id=domain.customer_id,
            content=domain.content,
            direction=domain.direction,
            source=domain.source,
            created_at=domain.created_at,
            automated=domain.automated,
            status=domain.status
        )
        return orm
