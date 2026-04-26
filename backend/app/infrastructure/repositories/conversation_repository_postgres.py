from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.conversation import Conversation
from domain.enums.conversation_status import ConversationStatus
from domain.enums.message_source import MessageSource
from domain.interfaces.conversation_repository import IConversationRepository
from infrastructure.mappers.conversation_mapper import ConversationMapper
from infrastructure.orm.conversation_orm import ConversationORM


class ConversationRepositoryPostgres(IConversationRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, conversation: Conversation) -> Conversation:
        orm = ConversationMapper.domain_to_orm(conversation)
        self.session.add(orm)
        await self.session.flush()
        await self.session.refresh(orm)
        return ConversationMapper.orm_to_domain(orm)

    async def update(self, conversation: Conversation) -> Conversation:
        orm = await self.session.get(ConversationORM, conversation.id)
        orm.status = conversation.status.value
        orm.assigned_agent_id = conversation.assigned_agent_id
        orm.updated_at = conversation.updated_at
        orm.resolved_at = conversation.resolved_at
        await self.session.flush()
        await self.session.refresh(orm)
        return ConversationMapper.orm_to_domain(orm)

    async def get_by_id(self, conversation_id: UUID) -> Conversation | None:
        orm = await self.session.get(ConversationORM, conversation_id)
        return ConversationMapper.orm_to_domain(orm) if orm else None

    async def get_active_by_customer(
        self,
        customer_id: int,
        source: MessageSource,
    ) -> Conversation | None:
        active_statuses = (
            ConversationStatus.BOT_HANDLING.value,
            ConversationStatus.ESCALATED.value,
            ConversationStatus.HUMAN_HANDLING.value,
        )
        result = await self.session.execute(
            select(ConversationORM)
            .where(
                ConversationORM.customer_id == customer_id,
                ConversationORM.source == source.value,
                ConversationORM.status.in_(active_statuses),
            )
            .limit(1)
        )
        orm = result.scalar_one_or_none()
        return ConversationMapper.orm_to_domain(orm) if orm else None

    async def list_by_status(
        self,
        status: ConversationStatus,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Conversation]:
        result = await self.session.execute(
            select(ConversationORM)
            .where(ConversationORM.status == status.value)
            .order_by(ConversationORM.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return [ConversationMapper.orm_to_domain(o) for o in result.scalars().all()]

    async def count_by_status(self, status: ConversationStatus) -> int:
        result = await self.session.execute(
            select(func.count()).where(ConversationORM.status == status.value)
        )
        return result.scalar_one()

    async def list_by_customer(
        self,
        customer_id: int,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Conversation]:
        result = await self.session.execute(
            select(ConversationORM)
            .where(ConversationORM.customer_id == customer_id)
            .order_by(ConversationORM.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return [ConversationMapper.orm_to_domain(o) for o in result.scalars().all()]
