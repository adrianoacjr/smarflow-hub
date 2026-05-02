from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True, slots=True)
class UpdateClientCommand:
    client_id: int
    name: Optional[str] = None
    email: Optional[str] = None
