import uuid
from sqlalchemy import Column, Integer, String, DateTime, ARRAY, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from infrastructure.orm.base import Base

class CustomerORM(Base):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("client.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, index=True, nullable=True)
    origin = Column(
        Enum(
            "whatsapp",
            "instagram",
            "import",
            "manual",
            name="customer_origin_enum"
        ),
        nullable=False
    )
    external_red = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    conversations = relationship("ConversationORM", back_populates="customer")
