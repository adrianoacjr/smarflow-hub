import secrets
import hashlib

from domain.entities.client import Client
from domain.interfaces.client_repository import IClientRepository
from domain.value_objects.email_address import EmailAddress
from domain.value_objects.phone_number import PhoneNumber
from application.dtos.client.client_item import ClientItem
from application.dtos.client.create_client_command import CreateClientCommand
from application.exceptions.client_exceptions import ClientAlreadyExistsError

class CreateClient:
    def __init__(self, repo: IClientRepository) -> None:
        self.repo = repo
    
    async def execute(self, command: CreateClientCommand) -> tuple[ClientItem, str]:
        email = EmailAddress(command.email)

        existing = await self.repo.get_by_email(email)
        if existing is not None:
            raise ClientAlreadyExistsError(
                f"A client with email '{command.email}' already exists."
            )

        phone = (
            PhoneNumber(command.phone)
            if command.phone is not None
            else None
        )
        
        raw_api_key = secrets.token_urlsafe(32)
        api_key_hash = hashlib.sha256(raw_api_key.encode()).hexdigest()

        client = Client(
            name=command.name.strip(),
            email=email,
            plan=command.plan,
            api_key_hash=api_key_hash,
            phone=phone,
        )

        saved = await self.repo.create(client)

        return ClientItem.from_entity(saved), raw_api_key
