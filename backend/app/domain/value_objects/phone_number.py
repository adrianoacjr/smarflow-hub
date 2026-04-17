from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class PhoneNumber:
    value: str

    def __post_init__(self) -> None:
        normalized = "".join(ch for ch in self.value if ch.isdigit() or ch == "+")

        if not normalized:
            raise ValueError("phone cannot be empty")
        
        if len([ch for ch in normalized if ch.isdigit()]) < 10:
            raise ValueError("invalid phone number")
        
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value
