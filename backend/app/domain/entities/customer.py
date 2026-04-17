from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from domain.enums.customer_origin import CustomerOrigin
from domain.value_objects.customer_tag import CustomerTag
from domain.value_objects.email_address import EmailAddress
from domain.value_objects.phone_number import PhoneNumber

@dataclass(eq=False, slots=True, kw_only=True)
class Customer:
    name: str
    origin: CustomerOrigin
    created_at: datetime
    tags: list[str] = field(default_factory=list)
    email: Optional[str] = None
    phone: Optional[str] = None
    id: Optional[int] = None

    def add_tag(self, tag: CustomerTag) -> None:
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: CustomerTag) -> None:
        self.tags = [item for item in self.tags if item != tag]
