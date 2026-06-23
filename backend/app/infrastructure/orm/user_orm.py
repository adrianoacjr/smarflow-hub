import uuid
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, UniqueConstraint, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from infrastructure.orm.base import Base

class UserORM(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("client_id", "email", name="uq_users_client_email"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("client.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    email = Column(String, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    access_level = Column(
        Enum("admin", "user", name="user_access_level_enum"),
        nullable=False,
    )
    user_type = Column(
        Enum("human", "bot", name="user_type_enum"),
        nullable=False,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    active = Column(Boolean, nullable=False, default=True)
    system_prompt = Column(Text, nullable=True)

    client = relationship("ClientORM", back_populates="users")
    channel_bindings = relationship(
        "UserChannelBindingORM",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    messages = relationship(
        "MessageORM",
        back_populates="user",
        foreign_keys="[MessageORM.user_id]",
    )
    bot_conversations = relationship(
        "ConversationORM",
        back_populates="bot_user",
        foreign_keys="[ConversationORM.bot_user_id]",
    )
    agent_conversations = relationship(
        "ConversationORM",
        back_populates="assigned_agent",
        foreign_keys="[ConversationORM.assigned_agent_id]",
    )
