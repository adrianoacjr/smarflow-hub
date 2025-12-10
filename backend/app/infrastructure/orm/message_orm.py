from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from infrastructure.orm.base import Base

class MessageORM(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    content = Column(String, nullable=False)
    direction = Column(
        Enum(
            "inbound",
            "outbound",
            name="direction_enum"
        ),
        nullable=False
    )
    source = Column(
        Enum(
            "whatsapp",
            "instagram",
            "other",
            name="source_enum"
        ),
        nullable=False
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    automated = Column(bool, nullable=False)
    status = Column(
        Enum(
            "sent",
            "delivered",
            "read",
            "failed"
        )
    )

    user = relationship("UserORM", back_populates="messages")
    customer = relationship("CustomerORM", back_populates="messages")
