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

class CustomerResponseDTO(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    origin: str
    tags: list[str]
    created_at: datetime

    @staticmethod
    def from_domain(customer: Customer):
        return CustomerResponseDTO(
            id=customer.id,
            name=customer.name,
            email=customer.email,
            phone=customer.phone,
            origin=customer.origin,
            tags=customer.tags,
            created_at=customer.created_at
        )
