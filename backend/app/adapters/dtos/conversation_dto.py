from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel

from domain.enums.conversation_status import ConversationStatus
from domain.enums.message_source import MessageSource

class ConversationResponseDTO(BaseModel):
    id: UUID
    client_id: int
    customer_id: int
    source: MessageSource
    status: ConversationStatus
    assigned_agent_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
    resolved_at: Optional[datetime]

    model_config = {"from_attributes": True}

class ConversationListResponseDTO(BaseModel):
    conversation: list[ConversationResponseDTO]
    total: int

class EscalateConversationRequestDTO(BaseModel):
    reason: Optional[str] = None
