from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ListMessagesByCustomerQuery:
    customer_id: int
    limit: int = 50
    offset: int = 0

@dataclass(frozen=True, slots=True)
class ListMessagesByUserQuery:
    user_id: int
    limit: int = 50
    offset: int = 0
