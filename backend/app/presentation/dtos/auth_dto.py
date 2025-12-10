from pydantic import BaseModel, Field, EmailStr

class LoginDTO(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)

class TokenResponseDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"
