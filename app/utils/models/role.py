from pydantic import BaseModel


class Role(BaseModel):
    # TODO: NAME
    permissions: list[str] = []