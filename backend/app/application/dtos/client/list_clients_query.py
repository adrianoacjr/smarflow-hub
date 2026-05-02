from dataclasses import dataclass

from domain.entities.client import Client

@dataclass(frozen=True, slots=True)
class ListClientQuery:
    items: tuple[Client, ...]
    total: int
    limit: int
    offset: int
