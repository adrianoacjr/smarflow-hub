from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True, slots=True)
class AnalyzeMessageCommand:
    inbound_message_id: UUID
