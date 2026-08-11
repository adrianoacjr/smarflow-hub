from dataclasses import dataclass

from domain.enums.client_plan import ClientPlan

@dataclass(frozen=True, slots=True)
class CreateClientCommand:
    name: str
    email: str
    plan: ClientPlan = ClientPlan.FREE
    phone: str | None = None
