from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
from uuid import UUID

class WhatsAppAttachmentDTO(BaseModel):
    url: str
    mime_type: str
    filename: Optional[str] = None

class WhatsAppWebhookDTO(BaseModel):
    """
    Payload enviado pelo Meta via webhook POST.

    user_id: UUID do bot (User) reponsável por este número de WhatsApp.
    source: canal de origem - sempre 'whatsapp' neste contexto.
    phone: número do cliente final (source_customer_ref).
    customer_name: nome do contato do WhtsApp (pode ser vazio).
    content: texto da mensagem (opcional se vier anexo).
    attachments: lista de mídia recebida.
    """
    user_id: UUID
    source: str = "whatsapp"
    phone: str
    customer_name: Optional[str] = None
    content: Optional[str] = None
    attachments: Optional[list[WhatsAppAttachmentDTO]] = None
