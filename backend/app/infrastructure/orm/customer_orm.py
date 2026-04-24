from sqlalchemy import Column, Integer, String, DateTime, ARRAY, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID
import uuid

from infrastructure.orm.base import Base

class CustomerORM(Base):
    __tablename__ = "customers"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, unique=True, index=True, nullable=True)
    origin = Column(
        Enum(
            "whatsapp",
            "instagram",
            "manual",
            "other",
            name="customer_origin_enum"
        ),
        nullable=False
    )
    source = Column(
        Enum("whatsapp", "instagram", "manual", "other", name="customer_source_enum")
    )
    source_ref = Column(String, nullable=True, index=True)
    tags = Column(ARRAY(String), nullable=True, default=[])
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    messages = relationship("MessageORM", back_populates="customers")
