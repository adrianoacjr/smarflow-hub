from dataclasses import dataclass, field

from domain.enums.message_source import MessageSource

@dataclass(frozen=True, slots=True)
class InboundAttachmentInput:
    url: str
    mime_type: str
    filename: str | None = None

@dataclass(frozen=True, slots=True)
class ReceiveMessageCommand:
    user_id: int
    source: MessageSource
    source_customer_ref: str
    customer_name: str | None = None
    content: str | None = None
    attachments: tuple[InboundAttachmentInput, ...] = field(default_factory=tuple)
    automated: bool = False
