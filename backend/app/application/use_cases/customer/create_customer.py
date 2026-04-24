from datetime import datetime, timezone

from domain.entities.customer import Customer
from domain.interfaces.customer_repository import ICustomerRepository
from domain.value_objects.email_address import EmailAddress
from domain.value_objects.phone_number import PhoneNumber
from application.dtos.customer.create_customer_command import CreateCustomerCommand

class CreateCustomer:
    def __init__(self, repo: ICustomerRepository):
        self.repo = repo

    async def execute(self, command: CreateCustomerCommand) -> Customer:
        new_customer = Customer(
            name = command.name.strip(),
            origin = command.origin,
            source = command.source,
            source_ref = command.source_ref,
            email = EmailAddress(command.email) if command.email else None,
            phone = PhoneNumber(command.phone) if command.phone else None,
            created_at = datetime.now(timezone.utc),
        )
        return await self.repo.create(new_customer)
