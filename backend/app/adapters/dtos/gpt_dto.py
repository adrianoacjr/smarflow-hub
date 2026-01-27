from pydantic import BaseModel, Field

class GPTRequestDTO(BaseModel):
    message: str = Field(..., min_length=1, description="Text to be processed by AI")
    customer_id: int = Field(..., gt=0, description="Customer identifier")

class GPTResponseDTO(BaseModel):
    response: str
