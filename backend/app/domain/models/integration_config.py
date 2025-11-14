from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional

class IntegrationConfig(BaseModel):
    id: Optional[int] = None
    user_id: int
    service: str = Field(..., pattern="^(whatsapp|instagram|gpt5)$")
    credentials: dict
    active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
