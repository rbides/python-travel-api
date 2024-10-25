from uuid import UUID

from sqlalchemy import update as sql_update
from app.database.models import UserEntity
from app.database import Session
from app.service.models import User, UserUpdate


def add(user: User):
    with Session.begin() as session:
        session.add(UserEntity(**user.model_dump()))

def update(id: UUID, user: UserUpdate):
    with Session.begin() as session:
        session.execute(
            sql_update(UserEntity)
                .where(UserEntity.id==id)
                .values(user.model_dump(exclude_none=True))
        )

def get() -> list[UserEntity]:
    with Session() as session:
        users = session.query(UserEntity).all()
    return users

def get_by_id(id: UUID) -> UserEntity:
    with Session() as session:
        user = session.query(UserEntity).get(id)
    return user

def delete(id: UUID):
    with Session.begin() as session:
        user = session.query(UserEntity).get(id)
        session.delete(user)
