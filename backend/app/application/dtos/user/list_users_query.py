from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ListUsersQuery:
    limit: int = 50
    offset: int = 0
