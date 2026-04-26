import uuid

from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from infrastructure.orm.base import Base


class UserORM(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
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

    messages = relationship(
        "MessageORM",
        back_populates="users",
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
