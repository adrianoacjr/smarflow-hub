from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.customer import Customer
from domain.enums.message_source import MessageSource
from domain.interfaces.customer_repository import ICustomerRepository
from domain.value_objects.email_address import EmailAddress
from domain.value_objects.phone_number import PhoneNumber
from infrastructure.mappers.customer_mapper import CustomerMapper
from infrastructure.orm.customer_orm import CustomerORM

class CustomerRepositoryPostgres(ICustomerRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, customer: Customer) -> Customer:
        orm_customer = CustomerMapper.domain_to_orm(customer)
        self.session.add(orm_customer)
        await self.session.flush()
        await self.session.refresh(orm_customer)
        return CustomerMapper.orm_to_domain(orm_customer)
    
    async def update(self, customer: Customer) -> Customer:
        orm = await self.session.get(CustomerORM, customer.id)
        orm.name = customer.name
        orm.email = customer.email.value if customer.email else None
        orm.phone = customer.phone.value if customer.phone else None
        orm.origin = customer.origin.value
        orm.source = customer.source.value if customer.source else None
        orm.source_ref = customer.source_ref
        orm.tags = [t.value for t in customer.tags] if customer.tags else []
        await self.session.flush()
        await self.session.refresh(orm)
        return CustomerMapper.orm_to_domain(orm)
    
    async def get_by_id(self, customer_id: int) -> Optional[Customer]:
        orm = await self.session.get(CustomerORM, customer_id)
        return CustomerMapper.orm_to_domain(orm) if orm else None
    
    async def get_by_email(self, email: EmailAddress) -> Optional[Customer]:
        result = await self.session.execute(
            select(CustomerORM).where(CustomerORM.email == email.value)
        )
        orm = result.scalar_one_or_none()
        return CustomerMapper.orm_to_domain(orm) if orm else None
    
    async def get_by_phone_number(self, phone: PhoneNumber) -> Optional[Customer]:
        result = await self.session.execute(
            select(CustomerORM).where(CustomerORM.phone == phone.value)
        )
        orm = result.scalar_one_or_none()
        return CustomerMapper.orm_to_domain(orm) if orm else None
    
    async def get_by_source_ref(
        self,
        source: MessageSource,
        source_customer_ref: str,
    ) -> Optional[Customer]:
        result = await self.session.execute(
            select(CustomerORM).where(
                CustomerORM.source == source.value,
                CustomerORM.source_ref == source_customer_ref,
            )
        )
        orm = result.scalar_one_or_none()
        return CustomerMapper.orm_to_domain(orm) if orm else None
    
    async def list(self, limit = 50, offset: int = 0) -> list[Customer]:
        result = await self.session.execute(
            select(CustomerORM)
            .order_by(CustomerORM.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return [CustomerMapper.orm_to_domain(o) for o in result.scalars().all()]
    
    async def count(self) -> int:
        result = await self.session.execute(select(func.count(CustomerORM.id)))
        return result.scalar_one()

    
    async def delete(self, customer_id: int) -> bool:
        orm = await self.session.get(CustomerORM, customer_id)
        if orm is None:
            return False
        await self.session.delete(orm)
        await self.session.flush()
        return True
