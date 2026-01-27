from fastapi import APIRouter, HTTPException, status

from adapters.dtos.auth_dto import LoginDTO, TokenResponseDTO
from application.use_cases.user.authenticate_user import AuthenticateUser

def build_auth_router(
    authenticate_user: AuthenticateUser,
) -> APIRouter:
    router = APIRouter()

    @router.post("/login", response_model=TokenResponseDTO)
    async def login(data: LoginDTO):
        token = await authenticate_user.execute(data.email, data.password)
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        return TokenResponseDTO(access_token=token)

    return router
