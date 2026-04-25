from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class EmailAddress:
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()

        if not normalized:
            raise ValueError("email cannot be empty")
        
        parts = normalized.split("@")

        if len(parts) != 2 or not parts[0] or not parts[1] or "." not in parts[1]:
            raise ValueError("invalid email")
        
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value
