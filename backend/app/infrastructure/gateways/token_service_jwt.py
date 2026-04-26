from datetime import timedelta

from jose import jwt, JWTError

from application.interfaces.token_service import ITokenService
from infrastructure.config import settings

class TokenServiceJWT(ITokenService):
    def __init__(self, secret_key: str, algorithm: str, expire_minutes: int) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def create_access_token(
        self,
        subject: str,
        expires_in: timedelta,
        extra_claims: dict | None = None,
    ) -> str:
        from domain.utils.time import utcnow

        expire = utcnow() + expires_in
        payload: dict = {"sub": subject, "exp": expire}

        if extra_claims:
            payload.update(extra_claims)

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_access_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError as e:
            raise ValueError("Invalid or expired token") from e
