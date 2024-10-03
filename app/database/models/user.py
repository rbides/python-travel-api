from sqlalchemy import UUID, Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database.models import Base

class UserEntity(Base):
    __tablename__ = 'users'

    id = Column(UUID, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), server_onupdate=func.now())