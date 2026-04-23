from dataclasses import dataclass
from enum import StrEnum
from typing import Optional

from domain.entities.conversation import Conversation
from domain.entities.message import Message

class AnalysisOutcome(StrEnum):
    AI_REPLIED = "ai_replied"
    ESCALATED_LOW_CONFIENCE = "escalated_low_confidence"
    ESCALATED_BY_REQUEST = "escalated_by_request"
    HUMAN_HANDLING = "human_handling"

@dataclass(frozen=True, slots=True)
class AnalyzeMessageResult:
    outcome: AnalysisOutcome
    inbound_message: Message
    conversation: Conversation
    outbound_message: Optional[Message] = None
