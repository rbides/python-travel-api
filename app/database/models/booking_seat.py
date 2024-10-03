from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.schema import PrimaryKeyConstraint

from app.database.models import Base

class BookingSeatEntity(Base):
    __tablename__ = 'booking_seats'

    booking_id = Column(UUID, ForeignKey("bookings.id"), primary_key=True)
    seat_id = Column(UUID, ForeignKey("seats.id"), primary_key=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), server_onupdate=func.now())

    __table_args__ = (
        PrimaryKeyConstraint('booking_id', 'seat_id'),
    )