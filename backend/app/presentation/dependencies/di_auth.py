from infrastructure.security.token_service_jwt import TokenServiceJWT
from application.user.authenticate_user import AuthenticateUser
from presentation.dependencies.di_user import di_user
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

SECRET_KEY = "your-secret-key"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

token_service = TokenServiceJWT(secret_key=SECRET_KEY)
repo = di_user._repo

authenticate_user_use_case = AuthenticateUser(repo = repo, token_service = token_service)

def login_dependency():
    return authenticate_user_use_case

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    print("asds")
    try:
        email = token_service.verify_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials"
        )

    user = repo.get_by_email(email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    
    return user
