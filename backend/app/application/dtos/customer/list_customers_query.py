from dataclasses import dataclass

from domain.entities.customer import Customer

@dataclass(frozen=True, slots=True)
class ListCustomerQuery:
    items: tuple[Customer, ...]
    total: int
    limit: int
    offset: int
