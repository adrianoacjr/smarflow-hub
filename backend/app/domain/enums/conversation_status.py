from enum import StrEnum

class ConversationStatus(StrEnum):
    BOT_HANDLING = "bot_handling"
    ESCALATED = "escalated"
    HUMAN_HANDLING = "human_handling"
    RESOLVED = "resolved"
    ABANDONED = "abandoned"
