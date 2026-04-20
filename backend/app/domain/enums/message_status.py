from enum import StrEnum

class MessageStatus(StrEnum):
    RECEIVED = "received"
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    ESCALATED = "escalated"
