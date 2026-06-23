import uuid
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from infrastructure.orm.base import Base

class UserChannelBindingORM(Base):
    __tablename__ = "user_channel_bindings"
    __table_args__ = (
        UniqueConstraint("source", "external_ref", name="uq_channel_bindings_source_ref"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    source = Column(String(32), nullable=False)
    external_ref = Column(String, nullable=False)

    user = relationship("UserORM", back_populates="channel_bindings")
