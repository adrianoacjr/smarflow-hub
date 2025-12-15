from datetime import datetime

from domain.models.customer import Customer
from domain.interfaces.customer_repository import ICustomerRepository

class CreateCustomer:
    def __init__(self, repo: ICustomerRepository):
        self.repo = repo

    async def execute(self, name: str, email: str, phone: str, origin: str, created_at: datetime, user_id: int) -> Customer:
        new_customer = Customer(
            user_id=user_id,
            name=name,
            email=email,
            phone=phone,
            origin=origin,
            created_at=created_at,
        )
        return await self.repo.create(new_customer)
