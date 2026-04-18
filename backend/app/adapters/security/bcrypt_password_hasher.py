import bcrypt

from application.interfaces.password_hasher import IPasswordHasher

class BcryptPasswordHasher(IPasswordHasher):
    def hash(self, plain_text: str) -> str:
        hashed_password = bcrypt.hashpw(
            plain_text.encode("utf-8"),
            bcrypt.gensalt(),
        )
        return hashed_password.decode("utf-8")
    
    def verify(self, plain_text: str, hashed_text: str) -> bool:
        return bcrypt.checkpw(
            plain_text.encode("utf-8"),
            hashed_text.encode("utf-8")
        )
