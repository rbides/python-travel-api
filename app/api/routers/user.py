import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.models.user import CreateUserRequest, UpdateUserRequest
from app.service import user as service
from app.service.errors.user import UserNotFoundException
from app.service.models.user import User, UserUpdate
from app.utils import auth

router = APIRouter(
    prefix="/users",
)


@router.get("", status_code=status.HTTP_200_OK)
def get_users() -> list[User]:
    return service.get()


@router.get("/me")
async def read_users_me(
    current_user: Annotated[User, Depends(service.get_current_user)],
):
    return current_user


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: uuid.UUID) -> User:
    try:
        return service.get_by_id(user_id)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.detail
        )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(request: CreateUserRequest):
    # TODO: Handle User already exists exception
    user = User(
        id=uuid.uuid4(),
        username=request.username,
        email=request.email,
    )
    service.create(user, auth.get_password_hash(request.password))


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: uuid.UUID, request: UpdateUserRequest):
    user = UserUpdate(
        username=request.username,
        email=request.email,
    )
    try:
        service.update(user_id, user)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.detail
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: uuid.UUID):
    try:
        service.delete(user_id)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.detail
        )
