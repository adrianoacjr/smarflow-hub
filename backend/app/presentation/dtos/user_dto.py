from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, timezone
from typing import Optional
from domain.models.user import User

class UserCreateDTO(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    password: str
    access_level: str = Field(..., pattern="^(admin|user|guest)$")
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserResponseDTO(BaseModel):
    id: int
    name: str
    email: str

    @staticmethod
    def from_domain(user: User):
        return UserResponseDTO(id=user.id, name=user.name, email=user.email)
