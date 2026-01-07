from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Message:
    customer_id: int
    content: str
    direction: str
    source: str
    created_at: datetime
    automated: bool
    status: str
    user_id: Optional[int] = None
    id: Optional[int] = None
