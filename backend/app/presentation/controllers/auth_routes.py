from sqlalchemy.ext.asyncio import AsyncSession

from application.user.authenticate_user import AuthenticateUser
from presentation.dependencies.di_auth import di_auth
from fastapi import APIRouter, Depends, HTTPException, status

from presentation.dtos.auth_dto import LoginDTO, TokenResponseDTO

from core.database import get_session

router = APIRouter()

@router.post("/login", response_model=TokenResponseDTO)
async def login(data: LoginDTO, session: AsyncSession = Depends(get_session)):
    service: AuthenticateUser = di_auth.get_get_current_user_service(session)
    token = await service.execute(data.email, data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    return TokenResponseDTO(access_token=token)
