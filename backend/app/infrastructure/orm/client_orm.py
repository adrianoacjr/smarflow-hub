from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from infrastructure.orm.base import Base

class ClientORM(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    plan = Column(
        Enum("free", "basic", "pro", "enterprise", name="client_plan_enum"),
        nullable=False,
        default="free",
    )
    api_key_hash = Column(String, unique=True, index=True, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    users = relationship("UserORM", back_populates="client")
    customers = relationship("CustomerORM", back_populates="client")
    conversations = relationship("ConversationORM", back_populates="client")
