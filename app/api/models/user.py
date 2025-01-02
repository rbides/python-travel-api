from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from app.utils.models.role import Role


class CreateUserRequest(BaseModel):
    username: str
    email: str # create value type
    password: str # TODO: add pass validation

class UpdateUserRequest(BaseModel):
    username: str | None = None
    email: str | None = None # create value type
