from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class MessageContent:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip()

        if not normalized:
            raise ValueError("message content cannot be empty")
        
        if len(normalized) > 5000:
            raise ValueError("message content too long")
        
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value
