from fastapi import APIRouter, HTTPException

from application.dtos.user_dto import UserCreateDTO, UserResponseDTO
from application.use_cases.user.create_user import CreateUser
from application.use_cases.user.delete_user import DeleteUser
from application.use_cases.user.get_all_users import GetAllUsers
from application.use_cases.user.get_user import GetUser

def build_user_router(
    create_user: CreateUser,
    get_user: GetUser,
    get_all_users: GetAllUsers,
    delete_user: DeleteUser,
) -> APIRouter:
    router = APIRouter()

    @router.post("/users/", response_model=UserResponseDTO)
    async def create(user_input: UserCreateDTO):
        user = await create_user.execute(
            user_input.name,
            user_input.email,
            user_input.password,
            access_level = user_input.access_level,
            created_at = user_input.created_at
        )
        return UserResponseDTO.from_domain(user)

    @router.get("/users/{user_id}", response_model=UserResponseDTO)
    def get(user_id: int):
        user = get_user.execute(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponseDTO.from_domain(user)

    @router.get("/users/", response_model=list[UserResponseDTO])
    def get_all():
        users = get_all_users.execute()
        return [UserResponseDTO.from_domain(user) for user in users]

    @router.delete("/users/{user_id}", status_code=204)
    def delete(user_id: int):
        delete_user.execute(user_id)
        return None
