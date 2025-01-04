from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, computed_field, field_validator

from app.utils.models.role import Role



class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    username: str
    password: str | None = None
    email: str # create value type
    role: Role | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    # @computed_field
    # @property
    # def permissions(self, **kwargs) -> list[str]:
    #     print("resrtes", kwargs)
    #     return []
    @field_validator('role', mode='before')
    def serialize_role(cls, v):
        # print(v.permissions)
        print(v)
        if v is None:
            return Role()
        permissions = []
        for p in v.permissions:
            permissions.append(p.permission)
        return Role(permissions=permissions)



class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None # create value type
    updated_at: datetime = datetime.now()