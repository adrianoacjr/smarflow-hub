from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True, slots=True)
class UpdateClientCommand:
    client_id: UUID
    name: str | None = None
    email: str | None = None
    phone: str | None = None
