from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from domain.entities.message import Message
from domain.interfaces.message_repository import IMessageRepository

from infrastructure.orm.message_orm import MessageORM
from infrastructure.mappers.message_mapper import MessageMapper

class MessageRepositoryPostgres(IMessageRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, message: Message) -> Message:
        orm_message = MessageMapper.domain_to_orm(message)
        self.session.add(orm_message)
        await self.session.commit()
        await self.session.refresh(orm_message)
        return MessageMapper.orm_to_domain(orm_message)
    
    async def get_by_id(self, message_id: int) -> Optional[Message]:
        result = await self.session.execute(
            select(MessageORM).where(MessageORM.id == message_id)
        )
        orm = result.scalar_one_or_none()
        return MessageMapper.orm_to_domain(orm) if orm else None
    
    async def list_by_user(self, user_id: int, limit: int = 50, offset: int = 0) -> List[Message]:
        q = select(MessageORM).where(MessageORM.user_id == user_id).order_by(MessageORM.created_at.desc()).limit(limit).offset(offset)
        result = await self.session.execute(q)
        orms = result.scalars().all()
        return [MessageMapper.orm_to_domain(o) for o in orms]
    
    async def list_by_customer(self, customer_id: int, limit: int = 50, offset: int = 0) -> List[Message]:
        q = select(MessageORM).where(MessageORM.customer_id == customer_id).order_by(MessageORM.created_at.desc()).limit(limit).offset(offset)
        result = await self.session.execute(q)
        orms = result.scalars().all()
        return [MessageMapper.orm_to_domain(o) for o in orms]
    
    async def delete(self, message_id: int) -> None:
        await self.session.execute(
            delete(MessageORM).where(MessageORM.id == message_id)
        )
        await self.session.commit()
