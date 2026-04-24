from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID
import uuid

from infrastructure.orm.base import Base

class UserORM(Base):
    __tablename__ = "users"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    access_level = Column(
        Enum(
            "admin",
            "user",
            "guest",
            name="user_access_level_enum"
        ),
        nullable=False
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    active = Column(Boolean, nullable=False)

    messages = relationship("MessageORM", back_populates="users")
