from sqlalchemy import Column, Integer, String, DateTime, ARRAY, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from infrastructure.orm.base import Base

class CustomerORM(Base):
    __tablename__ = "customers"
    __table_args__ = (
        UniqueConstraint("client_id", "email", name="uq_customers_client_email"),
        UniqueConstraint("client_id", "phone", name="uq_customers_client_phone"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    email = Column(String, index=True, nullable=True)
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
    source = Column(
        Enum("whatsapp", "instagram", "system", name="customer_source_enum"),
        nullable=True,
    )
    source_ref = Column(String, nullable=True, index=True)
    tags = Column(ARRAY(String), nullable=True, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    client = relationship("ClientORM", back_populates="customers")
    messages = relationship("MessageORM", back_populates="customer")
    conversations = relationship("ConversationORM", back_populates="customer")
