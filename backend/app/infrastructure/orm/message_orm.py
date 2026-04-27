import uuid

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from infrastructure.orm.base import Base


class MessageORM(Base):
    __tablename__ = "messages"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    conversation_id = Column(
        PGUUID(as_uuid=True),
        ForeignKey("conversations.id"),
        nullable=True,
        index=True,
    )
    content = Column(String, nullable=True)
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
    )
    automated = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship(
        "UserORM",
        back_populates="messages",
        foreign_keys=[user_id],
    )
    customer = relationship(
        "CustomerORM",
        back_populates="messages",
        foreign_keys=[customer_id],
    )

    messages = relationship(
        "MessageORM",
        foreign_keys="[MessageORM.conversation_id]",
        back_populates="conversation",
    )
