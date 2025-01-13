from typing import Annotated
from uuid import UUID

from fastapi import Depends

from app.api.models.auth import TokenData
from app.repository import user as repo
from app.service import auth
from app.service.models.user import User, UserUpdate


def get() -> list[User]:
    return repo.get()


def get_by_id(id: UUID) -> User:
    return repo.get_by_id(id)


def create(user: User, hashed_password: str):
    repo.add(user, hashed_password)


def update(id: UUID, user: UserUpdate):
    repo.update(id, user)


def delete(id: UUID):
    repo.delete(id)


# TODO: token_data should probably be at the api layer
async def get_current_user(
    token_data: Annotated[TokenData, Depends(auth.get_token_data)]
):
    user = repo.get_by_username(username=token_data.username)
    if user is None:
        raise  # TODO creds exception
    user.password = (
        None  # Workaround for removing password. TODO: find a better way
    )
    return User.model_validate(user)
