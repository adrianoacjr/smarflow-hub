from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional

class User(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1)
    email: str
    password_hash: str
    access_level: str = Field(..., pattern="^(admin|user|guest)$")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active: bool = True
