from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class AuthenticationResult:
    access_token: str
    token_type: str = "bearer"
