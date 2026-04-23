from domain.interfaces.customer_repository import ICustomerRepository
from application.exceptions.message_exceptions import CustomerNotFoundError

class DeleteCustomer:
    def __init__(self, customer_repo: ICustomerRepository) -> None:
        self.customer_repo = customer_repo

    async def execute(self, customer_id: int) -> None:
        customer = await self.customer_repo.get_by_id(customer_id)
        if customer is None:
            raise CustomerNotFoundError(f"Customer '{customer_id}' not found")
        await self.customer_repo.delete(customer_id)
