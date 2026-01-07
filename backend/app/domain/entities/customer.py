from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Customer:
    name: str
    origin: str
    created_at: datetime
    tags: list[str] = field(default_factory=list)
    email: Optional[str] = None
    phone: Optional[str] = None
    id: Optional[int] = None
