from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from application.dtos.user_dto import UserCreateDTO, UserResponseDTO
from application.use_cases.user.create_user import CreateUser
from application.use_cases.user.delete_user import DeleteUser
from application.use_cases.user.get_all_users import GetAllUsers
from application.use_cases.user.get_user import GetUser

from infrastructure.dependencies.di_user import di_user

from core.database import get_session

router = APIRouter()

@router.post("/users/", response_model=UserResponseDTO)
async def create_user(user_input: UserCreateDTO, session: AsyncSession = Depends(get_session)):
    service: CreateUser = di_user.get_create_user_service(session)
    user = await service.execute(
        user_input.name,
        user_input.email,
        user_input.password,
        access_level = user_input.access_level,
        created_at = user_input.created_at
    )
    return UserResponseDTO.from_domain(user)

@router.get("/users/{user_id}", response_model=UserResponseDTO)
def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    service: GetUser = di_user.get_get_user_service(session)
    user = service.execute(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponseDTO.from_domain(user)

@router.get("/users/", response_model=list[UserResponseDTO])
def get_all_users(session: AsyncSession = Depends(get_session)):
    service: GetAllUsers = di_user.get_get_all_users_service(session)
    users = service.execute()
    return [UserResponseDTO.from_domain(user) for user in users]

@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    service: DeleteUser = di_user.get_delete_user_service(session)
    service.execute(user_id)
    return None
