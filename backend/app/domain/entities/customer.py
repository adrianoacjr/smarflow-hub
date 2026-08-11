from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from domain.enums.customer_origin import CustomerOrigin
from domain.enums.message_source import MessageSource
from domain.value_objects.customer_tag import CustomerTag
from domain.value_objects.email_address import EmailAddress
from domain.value_objects.phone_number import PhoneNumber
from domain.utils.time import utcnow

@dataclass(eq=False, slots=True, kw_only=True)
class Customer:
    client_id: UUID = None
    name: str = ""
    origin: CustomerOrigin
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)
    tags: list[CustomerTag] = field(default_factory=list)
    active: bool = True
    source: Optional[MessageSource] = None
    source_ref: Optional[str] = None
    email: Optional[EmailAddress] = None
    phone: Optional[PhoneNumber] = None
    id: Optional[UUID] = field(default_factory=uuid4)

    def deactivate(self) -> None:
        self.active = False

    def activate(self) -> None:
        self.active = True

    def add_tag( self, tag: CustomerTag) -> None:
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: CustomerTag) -> None:
        self.tags = [item for item in self.tags if item != tag]
