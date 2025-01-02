from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class Travel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    destination: str
    price: float # TODO: Create value type
    departure: datetime
    created_at: datetime | None = None
    updated_at: datetime | None = None

class TravelUpdate(BaseModel):
    name: str | None = None
    destination: str | None = None
    price: float | None = None # TODO: Create value type
    departure: datetime | None = None
    updated_at: datetime = datetime.now()


class TravelFilters(BaseModel):
    name: str = Field(None, max_length=20)
    min_price: Decimal = Field(None, decimal_places=2)
    max_price: Decimal = Field(None, decimal_places=2)
    min_departure: datetime | None = None
    max_departure: datetime | None = None
    order_by: Literal["created_at", "updated_at", "departure"] = "departure"