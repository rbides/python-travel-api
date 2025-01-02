from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field

from app.service.models import TravelFilters

class CreateTravelRequest(BaseModel):
    name: str = Field(title="Travel name", min_length=5, max_length=50)
    destination: str = Field(title="Travel destination", min_length=5, max_length=50)
    price: Decimal = Field(title="Ticket price", decimal_places=2) # TODO: Create value type
    departure: datetime = Field(title="Departure date of the travel", gt=datetime.now())

class UpdateTravelRequest(BaseModel):
    name: str | None =  Field(None, title="Travel name", min_length=5, max_length=50)
    destination: str | None =  Field(None, title="Travel destination", min_length=5, max_length=50)
    price: Decimal | None =  Field(None, title="Ticket price", decimal_places=2) # TODO: Create value type
    departure: datetime | None =  Field(None, title="Departure date of the travel", gt=datetime.now())
