from sqlalchemy import Column, DateTime, Integer, Numeric, String, UUID
from sqlalchemy.sql import func
from app.database.models import Base

class TravelEntity(Base):
    __tablename__ = 'travels'

    id = Column(UUID, primary_key=True)
    name = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    price = Column(Numeric(5, 2), nullable=False)
    departure = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())