from pydantic import BaseModel
from typing import Optional, Field, emailstr
from datetime import datetime, timezone

class Customer(BaseModel):
    id: Optional[int] = None
    user_id: int
    name: str = Field(..., min_length=1)
    email: emailstr
    phone: Optional[str] = None
    origin: str = Field(..., pattern="^(whatsapp|instagram|manual|other)$")
    tags: Optional[list[str]] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
