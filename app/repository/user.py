from uuid import UUID

from pydantic import TypeAdapter
from sqlalchemy import update as sql_update

from app.database.models.user import UserEntity
from app.database.session import Session
from app.service.errors.user import UserNotFoundException
from app.service.models.user import User, UserUpdate


def add(user: User, hashed_password: str):
    with Session.begin() as session:
        # TODO: better handling password flow
        session.add(
            UserEntity(
                **user.model_dump(exclude="password"), password=hashed_password
            )
        )


def update(id: UUID, user: UserUpdate):
    with Session.begin() as session:
        query = session.execute(
            sql_update(UserEntity)
            .where(UserEntity.id == id)
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


def get_by_username(username: str) -> User:
    with Session() as session:
        user = (
            session.query(UserEntity)
            .where(UserEntity.username == username)
            .first()
        )
        # print(user.role.permissions[0].permission)
        if user is None:
            raise UserNotFoundException()
        user = User.model_validate(user)
    return user


def delete(id: UUID):
    with Session.begin() as session:
        user = session.query(UserEntity).get(id)
        if user is None:
            raise UserNotFoundException()
        session.delete(user)
