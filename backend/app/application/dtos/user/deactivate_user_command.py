from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class DeactivateUserCommand:
    user_id: int
