from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True, slots=True)
class UpdateCustomerCommand:
    customer_id: int
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
