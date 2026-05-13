import uuid

from sqlalchemy import Column, String, ForeignKey, UniqueConstraint, Integer
from sqlalchemy.orm import relationship

from infrastructure.orm.base import Base

class UserChannelBindingModel(Base):
    __tablename__ = "user_channel_bindings"
    __table_args__ = (
        UniqueConstraint("source", "external_ref", name="uq_channel_bindings_source_ref"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    source = Column(String(32), nullable=False)
    external_ref = Column(String(128), nullable=False)

    user = relationship("UserORM", back_populates="channel_bindings")
