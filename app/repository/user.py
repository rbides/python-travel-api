from uuid import UUID

from pydantic import TypeAdapter
from sqlalchemy import update as sql_update
from app.database.models import UserEntity
from app.database import Session
from app.service.errors import UserNotFoundException
from app.service.models import User, UserUpdate


def add(user: User):
    with Session.begin() as session:
        session.add(UserEntity(**user.model_dump()))

def update(id: UUID, user: UserUpdate):
    with Session.begin() as session:
        query = session.execute(
            sql_update(UserEntity)
                .where(UserEntity.id==id)
                .values(user.model_dump(exclude_none=True))
        )
        if query.rowcount == 0:
            raise UserNotFoundException()

def get() -> list[User]:
    with Session() as session:
        users = session.query(UserEntity).all()
    ta = TypeAdapter(list[User])
    return ta.validate_python(users)

def get_by_id(id: UUID) -> User:
    with Session() as session:
        user = session.query(UserEntity).get(id)
    if user is None:
        raise UserNotFoundException()
    return User.model_validate(user)

def delete(id: UUID):
    with Session.begin() as session:
        user = session.query(UserEntity).get(id)
        if user is None:
            raise UserNotFoundException()
        session.delete(user)
