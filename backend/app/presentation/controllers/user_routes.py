from presentation.dtos.user_dto import UserCreateDTO, UserResponseDTO
from presentation.dependencies.di_user import di_user
from application.user.create_user import CreateUser
from application.user.get_user import GetUser
from application.user.get_all_users import GetAllUsers
from application.user.delete_user import DeleteUser
from presentation.dependencies.di_auth import get_current_user
from domain.models.user import User
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter()

@router.post("/users/", response_model=UserResponseDTO)
def create_user(user_input: UserCreateDTO, create_user_use_case: CreateUser = Depends(di_user.get_create_user_service)):
    user = create_user_use_case.execute(user_input.name, user_input.email, user_input.password, access_level = user_input.access_level, created_at = user_input.created_at)
    return UserResponseDTO.from_domain(user)

@router.get("/users/me", response_model=UserResponseDTO)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponseDTO.from_domain(current_user)

@router.get("/users/{user_id}", response_model=UserResponseDTO)
def get_user(user_id: int, get_user_use_case: GetUser = Depends(di_user.get_get_user_service)):
    user = get_user_use_case.execute(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponseDTO.from_domain(user)

@router.get("/users/", response_model=list[UserResponseDTO])
def get_all_users(get_all_users_use_case: GetAllUsers = Depends(di_user.get_get_all_users_service)):
    users = get_all_users_use_case.execute()
    return [UserResponseDTO.from_domain(user) for user in users]

@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, delete_user_use_case: DeleteUser = Depends(di_user.get_delete_user_service)):
    delete_user_use_case.execute(user_id)
    return None
