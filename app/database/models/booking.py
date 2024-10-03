from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String, Numeric
from sqlalchemy.sql import func

from app.database.models import Base

class BookingEntity(Base):
    __tablename__ = 'bookings'

    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    travel_id = Column(UUID, ForeignKey("travels.id"), nullable=False)
    amount = Column(Numeric(7, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())