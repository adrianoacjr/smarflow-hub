from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True, slots=True)
class EscalateConversationCommand:
    conversation_id: UUID
    reason: str | None = None
