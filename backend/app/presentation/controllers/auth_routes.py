from application.user.authenticate_user import AuthenticateUser
from presentation.dependencies.di_auth import login_dependency
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), login_uc: AuthenticateUser = Depends(login_dependency)):
    token = login_uc.execute(form_data.username, form_data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    return {"access_token": token, "token_type": "bearer"}
