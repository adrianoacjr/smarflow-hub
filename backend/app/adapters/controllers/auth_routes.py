from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database import get_session
from infrastructure.dependencies.di_user import get_authenticate_user
from adapters.dtos.auth_dto import LoginDTO, TokenResponseDTO

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponseDTO)
async def login(
    data: LoginDTO,
    session: AsyncSession = Depends(get_session),
):
    use_case = get_authenticate_user(session)
    token = await use_case.execute(data.email, data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return TokenResponseDTO(access_token=token)
