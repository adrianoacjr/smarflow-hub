from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ChangeUserPasswordCommand:
    user_id: int
    current_password: str
    new_password: str
