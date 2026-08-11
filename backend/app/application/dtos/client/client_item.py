from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.entities.client import Client
from domain.enums.client_plan import ClientPlan

@dataclass(frozen=True, slots=True)
class ClientItem:
    id: UUID
    name: str
    email: str
    plan: ClientPlan
    active: bool
    phone: str | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, client: Client) -> "ClientItem":
        return cls(
            id=client.id,
            name=client.name,
            email=client.email.value,
            plan=client.active,
            phone=client.phone.value if client.phone else None,
            created_at=client.created_at,
            updated_at=client.updated_at,
        )
