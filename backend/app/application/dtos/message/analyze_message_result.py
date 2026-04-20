from dataclasses import dataclass
from enum import StrEnum

from domain.entities.message import Message

class AnalysisOutcome(StrEnum):
    AI_REPLIED = "ai_replied"
    ESCALATED_LOW_CONFIENCE = "escalated_low_confidence"
    ESCALATED_BY_REQUEST = "escalated_by_request"

@dataclass(frozen=True, slots=True)
class AnalyzeMessageResult:
    outcome: AnalysisOutcome
    inbound_message: Message
    outbound_message: Message | None = None
