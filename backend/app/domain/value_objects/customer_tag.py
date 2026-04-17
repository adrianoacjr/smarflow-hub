from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class CustomerTag:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()

        if not normalized:
            raise ValueError("tag cannot be empty")
        
        if len(normalized) > 30:
            raise ValueError("tag too long")
        
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value
