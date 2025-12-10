from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Message:
    user_id: int
    customer_id: int
    content: str
    direction: str
    source: str
    created_at: datetime
    automated: bool
    status: str
    id: Optional[int] = None
