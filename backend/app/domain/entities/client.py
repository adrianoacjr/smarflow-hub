from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from domain.enums.client_plan import ClientPlan
from domain.value_objects.email_address import EmailAddress
from domain.utils.time import utcnow

@dataclass(eq=False, losts=True, kw_only=True)
class Client:
    name: str
    email: EmailAddress
    plan: ClientPlan
    api_key_hash: str
    active: bool = True
    created_at: datetime = field(default_factory=utcnow)
    id: Optional[int] = None

    def deactivate(self) -> None:
        self.active = False

    def activate(self) -> None:
        self.active = True

    def upgrade_plan(self, new_plan: ClientPlan) -> None:
        if new_plan.value <= self.plan.value:
            raise ValueError(
                f"Use change_plan() para downgrade. "
                f"Plano atual: {self.plan}, solicitando: {new_plan}"
            )
        self.plan = new_plan

    def change_plan(self, new_plan: ClientPlan) -> None:
        self.plan = new_plan
