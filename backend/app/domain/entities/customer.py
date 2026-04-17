from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from domain.enums.customer_origin import CustomerOrigin

@dataclass(eq=False, slots=True, kw_only=True)
class Customer:
    name: str
    origin: CustomerOrigin
    created_at: datetime
    tags: list[str] = field(default_factory=list)
    email: Optional[str] = None
    phone: Optional[str] = None
    id: Optional[int] = None

    def add_tag(self, tag: str) -> None:
        normalized = tag.strip().lower()
        if not normalized:
            raise ValueError("tag cannot be empty")
        if normalized not in self.tags:
            self.tags.append(normalized)

    def remove_tag(self, tag: str) -> None:
        normalized = tag.strip().lower()
        self.tags = [item for item in self.tags if item != normalized]
