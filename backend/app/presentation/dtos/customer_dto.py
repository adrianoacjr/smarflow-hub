from datetime import datetime, timezone
from typing import Optional, List

from pydantic import BaseModel, Field, EmailStr

from domain.models.customer import Customer

class CustomerCreateDTO(BaseModel):
    name: str = Field(..., min_length=1)
    email: Optional[EmailStr]
    phone: Optional[str]
    origin: str = Field(..., pattern="^(whatsapp|instagram|manual|other)$")
    tags: List[str] = Field(default_factory=list) 
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserResponseDTO(BaseModel):

    @staticmethod
    def from_domain(user: User):
        return UserResponseDTO(

        )
