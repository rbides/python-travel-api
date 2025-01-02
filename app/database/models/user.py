from sqlalchemy import UUID, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.models import Base

class UserEntity(Base):
    __tablename__ = 'users'

    id = Column(UUID, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), server_onupdate=func.now())
    role_id = Column(UUID, ForeignKey("roles.id")) # TODO: fill this on creation ? Allowing it to be null seems more convenient

    role = relationship("RoleEntity")
    # permissions = relationship("RolePermissionsEntity", primaryjoin="UserEntity.role_id == RolePermissionsEntity.role_id") <- was not needed