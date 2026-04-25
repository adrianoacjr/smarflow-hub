from datetime import datetime, timezone

from domain.entities.customer import Customer
from domain.enums.customer_origin import CustomerOrigin
from domain.enums.message_source import MessageSource
from domain.interfaces.customer_repository import ICustomerRepository

class GetOrCreateCustomer:
    def __init__(self, repo: ICustomerRepository) -> None:
        self._repo = repo

    async def execute(
        self,
        source: MessageSource,
        source_ref: str,
        name: str | None = None,
    ) -> Customer:
        customer = await self._repo.get_by_source_ref(
            source=source,
            source_customer_ref=source_ref,
        )

        if customer is not None:
            return customer
        
        placeholder = Customer(
            name=name or source_ref,
            origin=CustomerOrigin.WHATSAPP if source == MessageSource.WHATSAPP else CustomerOrigin.INSTAGRAM,
            source=source,
            source_ref=source_ref,
            created_at=datetime.now(timezone.utc),
        )

        return await self._repo.create(placeholder)
