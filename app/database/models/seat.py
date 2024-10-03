from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func
from app.database.models import Base

class SeatEntity(Base):
    __tablename__ = 'seats'

    id = Column(UUID, primary_key=True)
    travel_id = Column(UUID, ForeignKey("travels.id"), nullable=False)
    position = Column(Integer, nullable=False)
    is_free = Column(Boolean, nullable=False, default=True) # Add a trigger to change value when booking is created?
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())