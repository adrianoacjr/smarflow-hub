import uuid
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from infrastructure.orm.base import Base

class ConversationORM(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("client.id"), nullable=False, index=True)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False, index=True)
    bot_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    assigned_agent_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    status = Column(
        Enum(
            "open",
            "bot_handling",
            "escalated",
            "human_handling",
            "closed",
            name="conversation_status_enum",
        ),
        nullable=False,
        default="open",
    )
    channel = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now())

    bot_user = relationship(
        "UserORM",
        back_populates="bot_conversations",
        foreign_keys=[bot_user_id],
    )
    assigned_agent = relationship(
        "UserORM",
        back_populates="agent_conversations",
        foreign_keys=[assigned_agent_id],
    )
    messages = relationship(
        "MessageORM",
        back_populates="conversation",
        cascade="all, delete-orphan"
    )
    customer = relationship(
        "CustomerORM",
        back_populates="conversations"
    )
