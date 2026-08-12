from domain.entities.client import Client
from domain.interfaces.client_repository import IClientRepository
from domain.value_objects.email_address import EmailAddress
from domain.value_objects.phone_number import PhoneNumber
from application.dtos.client.update_client_command import UpdateClientCommand
from application.exceptions.client_exceptions import (
    ClientNotFoundError,
    ClientAlreadyExistsError,
)

class UpdateClient:
    def __init__(self, repo: IClientRepository) -> None:
        self.repo = repo

    async def execute(self, command: UpdateClientCommand) -> Client:
        client = await self.repo.get_by_id(command.client_id)

        if client is None:
            raise ClientNotFoundError(
                f"Client '{command.client_id}' not found."
            )

        if command.name is not None:
            client.rename(command.name)

        if command.email is not None:
            new_email = EmailAddress(command.email)
            conflict = await self.repo.get_by_email(new_email)

            if conflict is not None and conflict.id != client.id:
                raise ClientAlreadyExistsError(
                    f"Email '{command.email}' is already in use."
                )

            client.change_email(new_email)

        if command.phone is not None:
            client.change_phone(PhoneNumber(command.phone))
        
        return await self.repo.update(client)
