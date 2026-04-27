import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from infrastructure.orm.base import Base


class ConversationORM(Base):
    __tablename__ = "conversations"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    bot_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_agent_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    source = Column(
        Enum("whatsapp", "instagram", "system", name="message_source_enum"),
        nullable=False,
    )
    status = Column(
        Enum(
            "bot_handling",
            "escalated",
            "human_handling",
            "resolved",
            "abandoned",
            name="conversation_status_enum",
        ),
        nullable=False,
    )
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    customer = relationship("CustomerORM", back_populates="conversations")
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
        foreign_keys="[MessageORM.conversation_id]",
        back_populates="conversation",
    )
