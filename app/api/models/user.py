from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    username: str
    email: str  # create value type
    password: str  # TODO: add pass validation


class UpdateUserRequest(BaseModel):
    username: str | None = None
    email: str | None = None  # create value type
