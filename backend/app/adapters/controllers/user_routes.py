from fastapi import APIRouter, HTTPException, Depends

from adapters.dtos.user_dto import UserCreateDTO, UserResponseDTO
from application.use_cases.user.create_user import CreateUser
from application.use_cases.user.delete_user import DeleteUser
from backend.app.application.use_cases.user.list_users import GetAllUsers
from application.use_cases.user.get_user import GetUser
from application.use_cases.user.update_user import UpdateUser
from infrastructure.dependencies.di_user import di_user

router = APIRouter()

@router.post("/users/", response_model=UserResponseDTO)
async def create(user_input: UserCreateDTO, use_case: CreateUser = Depends(di_user.get_create_user_use_case())):
    user = await use_case.execute(
        user_input.name,
        user_input.email,
        user_input.password,
        access_level = user_input.access_level,
        created_at = user_input.created_at
    )
    return UserResponseDTO.from_domain(user)

@router.get("/users/{user_id}", response_model=UserResponseDTO)
async def get(user_id: int, use_case: GetUser = Depends(di_user.get_get_user_use_case())):
    user = await use_case.execute(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponseDTO.from_domain(user)

@router.get("/users/", response_model=list[UserResponseDTO])
async def get_all(use_case: GetAllUsers = Depends(di_user.get_get_all_users_use_case())):
    users = await use_case.execute()
    return [UserResponseDTO.from_domain(user) for user in users]

@router.delete("/users/{user_id}", status_code=204)
async def delete(user_id: int, use_case: DeleteUser = Depends(di_user.get_delete_user_use_case())):
    await use_case.execute(user_id)
    return None
