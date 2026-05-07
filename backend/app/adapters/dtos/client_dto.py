from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class ClientCreateRequestDTO(BaseModel):
    name: str
    email: EmailStr
    plan: str

class ClientUpdateRequestDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class ClientChangePlanRequestDTO(BaseModel):
    plan: str

class ClientResponseDTO(BaseModel):
    id: UUID
    name: str
    email: str
    plan: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

class ClientCreateResponseDTO(ClientResponseDTO):
    api_key: str

class ClientListResponseDTO(BaseModel):
    clients: list[ClientResponseDTO]
