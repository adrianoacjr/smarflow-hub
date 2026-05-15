from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from domain.entities.user import User
from domain.enums.access_level import AccessLevel
from domain.enums.user_type import UserType

class UserCreateDTO(BaseModel):
    client_id: int
    name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=8)
    access_level: AccessLevel
    user_type: UserType
    system_prompt: Optional[str] = None

class UserResponseDTO(BaseModel):
    id: Optional[int]
    name: str
    email: str
    access_level: AccessLevel
    user_type: UserType
    created_at: datetime
    active: bool
    system_prompt: Optional[str] = None

    model_config = {"from_attributes": True}

    @staticmethod
    def from_domain(user: User) -> "UserResponseDTO":
        return UserResponseDTO(
            id=user.id,
            name=user.name,
            email=str(user.email),
            access_level=user.access_level,
            user_type=user.user_type,
            created_at=user.created_at,
            active=user.active,
            system_prompt=user.system_prompt,
        )
