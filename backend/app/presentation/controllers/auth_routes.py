from application.user.authenticate_user import AuthenticateUser
from infrastructure.repositories.user_repository_fake import UserRepositoryFake
from infrastructure.security.auth_utils import create_access_token
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

router = APIRouter()
repo = UserRepositoryFake()
auth_service = AuthenticateUser(repo)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_service.execute(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(data={"sub": str(user.id), "email": user.email}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
