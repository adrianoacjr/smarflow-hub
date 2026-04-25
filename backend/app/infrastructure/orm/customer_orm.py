from sqlalchemy import Column, Integer, String, DateTime, ARRAY, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from infrastructure.orm.base import Base

class CustomerORM(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, unique=True, index=True, nullable=True)
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
    source = Column(
        Enum("whatsapp", "instagram", "system", name="customer_source_enum"),
        nullable=True,
    )
    source_ref = Column(String, nullable=True, index=True)
    tags = Column(ARRAY(String), nullable=True, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    messages = relationship("MessageORM", back_populates="customers")
    conversations = relationship("ConversationORM", back_populates="customer")
