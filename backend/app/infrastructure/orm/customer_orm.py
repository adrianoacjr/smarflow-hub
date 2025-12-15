from sqlalchemy import Column, Integer, String, DateTime, ARRAY, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from infrastructure.orm.base import Base

class CustomerORM(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
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
    tags = Column(ARRAY(String), nullable=True, default=[])
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    messages = relationship("MessageORM", back_populates="customers")
