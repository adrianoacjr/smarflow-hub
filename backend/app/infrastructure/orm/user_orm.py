from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from infrastructure.orm.base import Base

class UserORM(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    access_level = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    active = Column(bool, nullable=False)
