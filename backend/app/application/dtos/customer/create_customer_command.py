from dataclasses import dataclass
from typing import Optional

from domain.enums.customer_origin import CustomerOrigin
from domain.enums.message_source import MessageSource

@dataclass(frozen=True, slots=True)
class CreateCustomerCommand:
    name: str
    origin: CustomerOrigin
    email: Optional[str] = None
    phone: Optional[str] = None
    source: Optional[MessageSource] = None
    source_ref: Optional[str] = None
