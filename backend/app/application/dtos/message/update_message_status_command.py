from dataclasses import dataclass
from uuid import UUID

from domain.enums.message_status import MessageStatus

@dataclass(frozen=True, slots=True)
class UpdateMessageStatusCommand:
    message_id: UUID
    status: MessageStatus
