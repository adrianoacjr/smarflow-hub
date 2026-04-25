from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, desc, func, select

from domain.entities.message import Message
from domain.interfaces.message_repository import IMessageRepository
from infrastructure.mappers.message_mapper import MessageMapper
from infrastructure.orm.message_orm import MessageORM

class MessageRepositoryPostgres(IMessageRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, message: Message) -> Message:
        orm_message = MessageMapper.domain_to_orm(message)
        self.session.add(orm_message)
        await self.session.flush()
        await self.session.refresh(orm_message)
        return MessageMapper.orm_to_domain(orm_message)
    
    async def update(self, message: Message) -> Message:
        orm = await self.session.get(MessageORM, message.id)
        orm.status = message.status.value
        orm.content = message.content.value if message.content else None
        await self.session.flush()
        await self.session.refresh(orm)
        return MessageMapper.orm_to_domain(orm)
    
    async def get_by_id(self, message_id: UUID) -> Message | None:
        orm = await self.session.get(MessageORM, message_id)
        return MessageMapper.orm_to_domain(orm) if orm else None
    
    async def list_by_customer(
        self,
        customer_id: int,
        limit: int = 50,
        offset: int = 0,
        order_by_created_asc: bool = True,
    ) -> list[Message]:
        order = asc(MessageORM.created_at) if order_by_created_asc else desc(MessageORM.created_at)
        result = await self.session.execute(
            select(MessageORM)
            .where(MessageORM.customer_id == customer_id)
            .order_by(order)
            .limit(limit)
            .offset(offset)
        )
        return [MessageMapper.orm_to_domain(o) for o in result.scalars().all()]
    
    async def count_by_customer(self, customer_id: int) -> int:
        result = await self.session.execute(
            select(func.count()).where(MessageORM.customer_id == customer_id)
        )
        return result.scalar_one()
    
    async def list_by_user(
        self,
        user_id: int,
        limit: int = 50,
        offset: int = 0
    ) -> list[Message]:
        result = await self.session.execute(
            select(MessageORM)
            .where(MessageORM.user_id == user_id)
            .order_by(desc(MessageORM.created_at))
            .limit(limit)
            .offset(offset)
        )
        return [MessageMapper.orm_to_domain(o) for o in result.scalars().all()]
    
    async def count_by_user(self, user_id: int) -> int:
        result = await self.session.execute(
            select(func.count()).where(MessageORM.user_id == user_id)
        )
        return result.scalar_one()
    
    async def list_by_conversation(
        self,
        conversation_id: UUID,
        limit: int = 50,
        offset: int = 0,
        order_by_created_asc: bool = True,
    ) -> list[Message]:
        order = asc(MessageORM.created_at) if order_by_created_asc else desc(MessageORM.created_at)
        result = await self.session.execute(
            select(MessageORM)
            .where(MessageORM.conversation_id == conversation_id)
            .order_by(order)
            .limit(limit)
            .offset(offset)
        )
        return [MessageMapper.orm_to_domain(o) for o in result.scalars().all()]
    
    async def delete(self, message_id: UUID) -> bool:
        orm = await self.session.get(MessageORM, message_id)
        if orm is None:
            return False
        await self.session.delete(orm)
        await self.session.flush()
        return True
