from pydantic import BaseModel

class WhatsAppWebhookDTO(BaseModel):
    phone: str
    content: str
