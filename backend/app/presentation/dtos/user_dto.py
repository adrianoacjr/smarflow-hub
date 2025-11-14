from pydantic import BaseModel
from domain.models.user import User

class UserCreateDTO(BaseModel):
    name: str
    email: str
    password: str
    access_level: str

class UserResponseDTO(BaseModel):
    id: int
    name: str
    email: str

    @staticmethod
    def from_domain(user: User):
        return UserResponseDTO(id=user.id, name=user.name, email=user.email)
