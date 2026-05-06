from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.dtos.user_dto import UserCreateDTO, UserResponseDTO
from infrastructure.database import get_session
from infrastructure.dependencies.di_user import (
    get_create_user,
    get_get_user,
    get_list_users,
    get_update_user,
    get_deactivate_user,
    get_delete_user,
    get_change_user_password,
)

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponseDTO, status_code=201)
async def create(
    body: UserCreateDTO,
    session: AsyncSession = Depends(get_session)
):
    use_case = get_create_user(session)
    user = await use_case.execute(
        name=body.name,
        email=body.email,
        password=body.password,
        access_level=body.access_level,
    )
    return UserResponseDTO.from_domain(user)

@router.get("/{user_id}", response_model=UserResponseDTO)
async def get(
    user_id: int,
    session: AsyncSession = Depends(get_session)
):
    use_case = get_get_user(session)
    user = await use_case.execute(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponseDTO.from_domain(user)

@router.get("/", response_model=list[UserResponseDTO])
async def get_all(
    session: AsyncSession = Depends(get_session)
):
    use_case = get_list_users(session)
    users = await use_case.execute()
    return [UserResponseDTO.from_domain(user) for user in users]

@router.delete("/{user_id}", status_code=204)
async def delete(
    user_id: int,
    session: AsyncSession = Depends(get_session)
):
    use_case = get_delete_user(session)
    await use_case.execute(user_id)
