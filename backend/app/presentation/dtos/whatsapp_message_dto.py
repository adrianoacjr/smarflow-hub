from pydantic import BaseModel

class whatsappMessageRequest(BaseModel):
    phone_number: str
    content: str

class whatsappMessageResponse(BaseModel):
    success: bool
    content: str
