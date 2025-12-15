from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Customer:
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    origin: str
    tags: list[str] = field(default_factory=list)
    created_at: datetime
    id: Optional[int] = None
