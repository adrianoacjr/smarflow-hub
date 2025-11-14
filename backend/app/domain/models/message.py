from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import Optional

class Message(BaseModel):
    id: Optional[int] = None
    user_id: int
    customer_id: int
    content: str = Field(..., max_length=1000)
    direction: str = Field(..., pattern="^(inbound|outbound)$")
    source: str = Field(..., pattern="^(whatsapp|instagram|other)$")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    automated: bool = False
    status: str = Field(..., pattern="^(sent|delivered|read|failed)$")
