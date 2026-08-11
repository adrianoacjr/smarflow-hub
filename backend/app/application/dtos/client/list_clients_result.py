from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

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

@dataclass(frozen=True, slots=True)
class ListClientsResult:
    items: tuple[ClientItem, ...]
    total: int
    limit: int
    offset: int
