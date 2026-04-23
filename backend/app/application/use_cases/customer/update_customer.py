from dataclasses import dataclass
from typing import Optional

from domain.entities.customer import Customer
from domain.interfaces.customer_repository import ICustomerRepository
from domain.value_objects.email_address import EmailAddress
from domain.value_objects.phone_number import PhoneNumber
from application.exceptions.message_exceptions import CustomerNotFoundError
from application.dtos.customer.update_customer_command import UpdateCustomerCommand

class UpdateCustomer:
    def __init__(self, customer_repo: ICustomerRepository) -> None:
        self.customer_repo = customer_repo

    async def execute(self, command: UpdateCustomerCommand) -> Customer:
        customer = await self.customer_repo.get_by_id(command.customer_id)
        if customer is None:
            raise CustomerNotFoundError(f"Customer '{command.customer_id}' not found")
        
        if command.name is not None:
            customer.name = command.name
        if command.email is not None:
            customer.email = EmailAddress(command.email)
        if command.phone is not None:
            customer.phone = PhoneNumber(command.phone)

        return await self.customer_repo.update(customer)
