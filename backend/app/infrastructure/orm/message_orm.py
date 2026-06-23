import uuid
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from infrastructure.orm.base import Base

class MessageORM(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"),
                             nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    direction = Column(
        Enum("inbound", "outbound", name="message_direction_enum"),
        nullable=False,
    )
    source = Column(
        Enum("whatsapp", "instagram", "system", name="message_source_enum"),
        nullable=False,
    )
    status = Column(
        Enum(
            "received",
            "pending",
            "sent",
            "delivered",
            "failed",
            "escalated",
            name="message_status_enum",
        ),
        nullable=False,
        default="pending",
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    conversation = relationship(
        "ConversationORM",
        back_populates="messages",
    )
    user = relationship(
        "UserORM",
        back_populates="messages",
        foreign_keys=[user_id],
    )
