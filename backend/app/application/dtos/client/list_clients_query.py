from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ListClientQuery:
    limit: int = 50
    offset: int = 0
