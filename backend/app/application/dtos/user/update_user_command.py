from dataclasses import dataclass

from domain.enums.access_level import AccessLevel

@dataclass(frozen=True, slots=True)
class UpdateUserCommand:
    user_id: int
    name: str | None = None
    email: str | None = None
    access_level: AccessLevel | None = None
