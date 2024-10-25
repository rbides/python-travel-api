from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    username: str
    email: str # create value type
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None # create value type
    updated_at: datetime = datetime.now()