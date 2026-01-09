from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from domain.entities.user import User

class UserCreateDTO(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=1)
    access_level: str = Field(..., pattern="^(admin|user|guest)$")
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserResponseDTO(BaseModel):
    id: int
    name: str
    email: str
    access_level: str
    created_at: datetime
    active: bool

    @staticmethod
    def from_domain(user: User):
        return UserResponseDTO(
            id=user.id,
            name=user.name,
            email=user.email,
            access_level=user.access_level,
            created_at=user.created_at,
            active=user.active
        )
