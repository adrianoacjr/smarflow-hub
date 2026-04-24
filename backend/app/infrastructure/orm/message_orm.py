from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID
import uuid

from infrastructure.orm.base import Base

class MessageORM(Base):
    __tablename__ = "messages"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    content = Column(String, nullable=True)
    direction = Column(
        Enum(
            "inbound",
            "outbound",
            name="message_direction_enum"
        ),
        nullable=False
    )
    source = Column(
        Enum(
            "whatsapp",
            "instagram",
            "other",
            name="message_source_enum"
        ),
        nullable=False
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    automated = Column(Boolean, nullable=False)
    status = Column(
        Enum(
            # Estados internos
            "created",        # criado no sistema
            "queued",         # pronto para envio
            "sending",        # tentando enviar
            "received",

            # Estados externos comuns
            "sent",
            "delivered",
            "read",

            # Estados de falha
            "failed",
            "rejected",
            "expired",
            "blocked",

            # Estados especiais
            "deleted",
            "unsupported",

            name="message_status_enum"
        )
    )

    users = relationship("UserORM", back_populates="messages")
    customers = relationship("CustomerORM", back_populates="messages")
