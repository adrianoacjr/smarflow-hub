from pydantic import BaseModel, Field

class GPTRequestDTO(BaseModel):
    message: str = Field(..., min_length=1, description="Text to be processed by AI")

class GPTResponseDTO(BaseModel):
    response: str
