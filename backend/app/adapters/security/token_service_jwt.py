from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError

from application.interfaces.token_service import ITokenService
from adapters.security.jwt_config import JWT_SECRET_KEY
from adapters.security.jwt_config import JwT_ALGORITHM
from adapters.security.jwt_config import ACCESS_TOKEN_EXPIRE_MINUTES
from adapters.security.jwt_config import REFRESH_TOKEN_EXPIRE_DAYS

class TokenServiceJWT(ITokenService):
    def __init__(self):
        self.secret_key = JWT_SECRET_KEY
        self.algorithm = JwT_ALGORITHM

    def create_access_token(self, subject: str) -> str:
        payload = {
            "sub": subject,
            "type": "access",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            "iat": datetime.now(timezone.utc),
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_access_token(self, token: str) -> str:
        try:
            decoded = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if decoded.get("type") != "access":
                raise ValueError("Invalid token type")
            return decoded["sub"]
        except JWTError:
            raise ValueError("Invalid or expired token")
