from dataclasses import dataclass

from domain.enums.access_level import AccessLevel
from domain.enums.user_type import UserType

@dataclass(frozen=True, slots=True)
class CreateUserCommand:
    name: str
    email: str
    password: str
    access_level: AccessLevel
    user_type: UserType = UserType.HUMAN
