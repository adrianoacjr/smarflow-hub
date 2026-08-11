from dataclasses import dataclass

from .client_item import ClientItem

@dataclass(frozen=True, slots=True)
class ListClientResult:
    items: tuple[ClientItem, ...]
    total: int
    limit: int
    offset: int
