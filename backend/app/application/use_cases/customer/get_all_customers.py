from dataclasses import dataclass

from domain.entities.customer import Customer
from domain.interfaces.customer_repository import ICustomerRepository
from application.dtos.customer.list_customers_query import ListCustomerQuery

class GetAllCustomers:
    def __init__(self, customer_repo: ICustomerRepository) -> None:
        self.customer_repo = customer_repo

    async def execute(self, limit: int = 50, offset: int = 0) -> ListCustomerQuery:
        items = await self.customer_repo.list(limit = limit, offset = offset)
        total = await self.customer_repo.count()
        return ListCustomerQuery(
            items = tuple(items),
            total = total,
            limit = limit,
            offset = offset,
        )
