from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class Travel(BaseModel):
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
