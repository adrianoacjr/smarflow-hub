from application.user.authenticate_user import AuthenticateUser
from presentation.dependencies.di_auth import login_dependency
from fastapi import APIRouter, Depends, HTTPException, status

from presentation.dtos.auth_dto import LoginDTO, TokenResponseDTO

router = APIRouter()

@router.post("/login", response_model=TokenResponseDTO)
def login(data: LoginDTO, login_uc: AuthenticateUser = Depends(login_dependency)):
    token = login_uc.execute(data.email, data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    return TokenResponseDTO(access_token=token)
