from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from domain.enums.access_level import AccessLevel

@dataclass(eq=False, slots=True, kw_only=True)
class User:
    name: str
    email: str
    password_hash: str = field(repr=False)
    access_level: AccessLevel
    created_at: datetime
    active: bool = True
    id: Optional[int] = None

    def deactivate(self) -> None:
        self.active = False

    def activate(self) -> None:
        self.active = True

    def change_access_level(self, access_level: AccessLevel) -> None:
        self.access_level = access_level
