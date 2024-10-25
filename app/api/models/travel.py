from datetime import datetime
from pydantic import BaseModel


class CreateTravelRequest(BaseModel):
    name: str
    destination: str
    price: float # TODO: Create value type
    departure: datetime

class UpdateTravelRequest(BaseModel):
    name: str | None = None
    destination: str | None = None
    price: float | None = None # TODO: Create value type
    departure: datetime | None = None