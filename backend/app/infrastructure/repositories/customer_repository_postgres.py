from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from domain.models.customer import Customer
from domain.interfaces.customer_repository import ICustomerRepository

from infrastructure.orm.customer_orm import CustomerORM
from infrastructure.orm.customer_mapper import CustomerMapper

class CustomerRepositoryPostgres(ICustomerRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, customer: Customer) -> Customer:
        orm_customer = CustomerMapper.domain_to_orm(customer)
        self.session.add(orm_customer)
        await self.session.commit()
        await self.session.refresh(orm_customer)
        return CustomerMapper.orm_to_domain(orm_customer)
    
    async def get_by_id(self, customer_id: int) -> Optional[Customer]:
        result = await self.session.execute(
            select(CustomerORM).where(CustomerORM.id == customer_id)
        )
        orm = result.scalar_one_or_none()
        return CustomerMapper.orm_to_domain(orm) if orm else None
    
    async def get_by_email(self, email: str) -> Optional[Customer]:
        result = await self.session.execute(
            select(CustomerORM).where(CustomerORM.email == email)
        )
        orm = result.scalar_one_or_none()
        return CustomerMapper.orm_to_domain(orm) if orm else None
    
    async def get_by_phone_number(self, phone: str) -> Optional[Customer]:
        result = await self.session.execute(
            select(CustomerORM).where(CustomerORM.phone == phone)
        )
        orm = result.scalar_one_or_none()
        return CustomerMapper.orm_to_domain(orm) if orm else None
    
    async def list(self) -> List[Customer]:
        result = await self.session.execute(select(CustomerORM))
        orms = result.scalars().all()
        return [CustomerMapper.orm_to_domain(o) for o in orms]
    
    async def delete(self, customer_id: int) -> None:
        await self.session.execute(
            delete(CustomerORM).where(CustomerORM.id == customer_id)
        )
        await self.session.commit()
