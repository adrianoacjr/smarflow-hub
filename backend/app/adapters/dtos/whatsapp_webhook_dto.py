from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
from uuid import UUID

class WhatsAppAttachmentDTO(BaseModel):
    url: str
    mime_type: str
    filename: Optional[str] = None

class WhatsAppWebhookDTO(BaseModel):
    phone_number_id: str
    source: str = "whatsapp"
    phone: str
    customer_name: Optional[str] = None
    content: Optional[str] = None
    attachments: Optional[list[WhatsAppAttachmentDTO]] = None
