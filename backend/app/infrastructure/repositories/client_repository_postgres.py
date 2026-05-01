from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.client import Client
from domain.interfaces.client_repository import IClientRepository
from domain.value_objects.email_address import EmailAddress
from infrastructure.mappers.client_mapper import ClientMapper
from infrastructure.orm.client_orm import ClientORM

class ClientRepositoryPostgres(IClientRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, client: Client) -> Client:
        orm_client = ClientMapper.domain_to_orm(client)
        self.session.add(orm_client)
        await self.session.flush()
        await self.session.refresh(orm_client)
        return ClientMapper.orm_to_domain(orm_client)
    
    async def update(self, client: Client) -> Client:
        orm = await self.session.get(ClientORM, client.id)
        orm.name = client.name
        orm.email = client.email.value
        orm.plan = client.plan.value
        orm.api_key_hash = client.api_key_hash
        orm.active = client.active
        await self.session.flush()
        await self.session.refresh(orm)
        return ClientMapper.orm_to_domain(orm)
    
    async def get_by_id(self, client_id: int) -> Optional[Client]:
        orm = await self.session.get(ClientORM, client_id)
        return ClientMapper.orm_to_domain(orm) if orm else None
    
    async def get_by_email(self, email: EmailAddress) -> Optional[Client]:
        result = await self.session.execute(
            select(ClientORM).where(ClientORM.email == email.value)
        )
        orm = result.scalar_one_or_none()
        return ClientMapper.orm_to_domain(orm) if orm else None
    
    async def get_by_api_key_hash(self, api_key_hash: str) -> Optional[Client]:
        result = await self.session.execute(
            select(ClientORM).where(ClientORM.api_key_hash == api_key_hash)
        )
        orm = result.scalar_one_or_none()
        return ClientMapper.orm_to_domain(orm) if orm else None
    
    async def list (self, limit: int = 50, offset: int = 0) -> list[Client]:
        result = await self.session.execute(
            select(ClientORM)
            .where(ClientORM.active == True)
            .order_by(ClientORM.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return [ClientMapper.orm_to_domain(o) for o in result.scalars().all()]
    
    async def count(self) -> int:
        result = await self.session.execute(
            select(func.count(ClientORM.id))
        )
        return result.scalar_one()
    
    async def delete(self, client_id: int) -> bool:
        orm = await self.session.get(ClientORM, client_id)
        if orm is None:
            return False
        await self.session.delete(orm)
        await self.session.flush()
        return True
