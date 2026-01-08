# from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status

from application.dtos.auth_dto import LoginDTO, TokenResponseDTO
from application.use_cases.user.authenticate_user import AuthenticateUser

# from infrastructure.dependencies.di_auth import di_auth

# from core.database import get_session

def build_auth_router(
    authenticate_user: AuthenticateUser,
) -> APIRouter:
    router = APIRouter()

    @router.post("/login", response_model=TokenResponseDTO)
    # async def login(data: LoginDTO, session: AsyncSession = Depends(get_session)):
    #     service: AuthenticateUser = di_auth.get_get_current_user_service(session)
    async def login(data: LoginDTO):
        token = await authenticate_user.execute(data.email, data.password)
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        return TokenResponseDTO(access_token=token)
