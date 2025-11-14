from domain.interfaces.token_service import ITokenService
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

class TokenServiceJWT(ITokenService):
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(self, subject: str, expires_in: timedelta) -> str:
        payload = {
            "sub": subject,
            "exp": datetime.now(timezone.utc) + expires_in
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_access_token(self, token: str) -> str:
        try:
            decoded = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return decoded["sub"]
        except JWTError:
            raise ValueError("Invalid or expired token")
