from domain.entities.customer import Customer
from domain.interfaces.customer_repository import ICustomerRepository
from application.exceptions.message_exceptions import CustomerNotFoundError

class GetCustomer:
    def __init__(self, customer_repo: ICustomerRepository) -> None:
        self.customer_repo = customer_repo

    async def execute(self, customer_id: int) -> Customer:
        customer = await self.customer_repo.get_by_id(customer_id)
        if customer is None:
            raise CustomerNotFoundError(f"Customer '{customer_id}' not found")
        return customer
