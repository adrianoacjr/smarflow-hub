from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.user import User
from domain.interfaces.user_repository import IUserRepository
from domain.value_objects.email_address import EmailAddress
from infrastructure.mappers.user_mapper import UserMapper
from infrastructure.orm.user_orm import UserORM

class UserRepositoryPostgres(IUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user: User) -> User:
        orm_user = UserMapper.domain_to_orm(user)
        self.session.add(orm_user)
        await self.session.flush()
        await self.session.refresh(orm_user)
        return UserMapper.orm_to_domain(orm_user)
    
    async def update(self, user: User) -> User:
        orm = await self.session.get(UserORM, user.id)
        orm.name = user.name
        orm.email = user.email.value
        orm.access_level = user.access_level.value
        orm.user_type = user.user_type.value
        orm.active = user.active
        await self.session.flush()
        await self.session.refresh(orm)
        return UserMapper.orm_to_domain(orm)
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        orm = await self.session.get(UserORM, user_id)
        return UserMapper.orm_to_domain(orm) if orm else None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(UserORM).where(UserORM.email == email.value)
        )
        orm = result.scalar_one_or_none()
        return UserMapper.orm_to_domain(orm) if orm else None
    
    async def list(self, limit = 50, offset: int = 0) -> list[User]:
        result = await self.session.execute(
            select(UserORM)
            .order_by(UserORM.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return [UserMapper.orm_to_domain(o) for o in result.scalars().all()]
    
    async def delete(self, user_id: int) -> bool:
        orm = await self.session.get(UserORM, user_id)
        if orm is None:
            return False
        await self.session.delete(orm)
        await self.session.flush()
        await True
