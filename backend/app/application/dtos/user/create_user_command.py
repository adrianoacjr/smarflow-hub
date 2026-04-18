from dataclasses import dataclass

from domain.enums.access_level import AccessLevel

@dataclass(frozen=True, slots=True)
class CreateUserCommand:
    name: str
    email: str
    password: str
    access_level: AccessLevel
