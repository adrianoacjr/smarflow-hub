from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    name: str
    email: str
    password_hash: str
    access_level: str
    created_at: datetime
    active: bool = True
    id: Optional[int] = None
