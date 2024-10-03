from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.sql import func

from app.database.models import Base

class PaymentEntity(Base):
    __tablename__ = 'payments'

    id = Column(UUID, primary_key=True)
    booking_id = Column(UUID, ForeignKey("bookings.id"), nullable=False)
    amount = Column(Numeric(7, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())