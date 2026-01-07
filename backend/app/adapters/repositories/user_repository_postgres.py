from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from domain.entities.user import User
from domain.interfaces.user_repository import IUserRepository

from infrastructure.orm.user_orm import UserORM
from adapters.mappers.user_mapper import UserMapper

class UserRepositoryPostgres(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        orm_user = UserMapper.domain_to_orm(user)
        self.session.add(orm_user)
        await self.session.commit()
        await self.session.refresh(orm_user)
        return UserMapper.orm_to_domain(orm_user)
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(UserORM).where(UserORM.id == user_id)
        )
        orm = result.scalar_one_or_none()
        return UserMapper.orm_to_domain(orm) if orm else None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(
            select(UserORM).where(UserORM.email == email)
        )
        orm = result.scalar_one_or_none()
        return UserMapper.orm_to_domain(orm) if orm else None
    
    async def list(self) -> List[User]:
        result = await self.session.execute(select(UserORM))
        orms = result.scalars().all()
        return [UserMapper.orm_to_domain(o) for o in orms]
    
    async def delete(self, user_id: int) -> None:
        await self.session.execute(
            delete(UserORM).where(UserORM.id == user_id)
        )
        await self.session.commit()
