from infrastructure.security.auth_utils import SECRET_KEY, ALGORITHM
from domain.models.user import User
from infrastructure.repositories.user_repository_fake import UserRepositoryFake
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

repo = UserRepositoryFake()

def get_current_user(token: str=Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = repo.get_by_id(int(user_id))
    if user is None:
        raise credentials_exception
    return user
