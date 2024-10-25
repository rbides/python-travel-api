import uuid
from fastapi import APIRouter
from app.api.models.user import CreateUserRequest, UpdateUserRequest
from app.service import user as service
from app.service.models import User, UserUpdate


router = APIRouter(
    prefix="/users",
)


@router.get("")
def get_users():
    return service.get()


@router.get("/{user_id}")
def get_user(user_id: uuid.UUID):
    return service.get_by_id(user_id)


@router.post("")
def create_user(request: CreateUserRequest):
    user = User(
        id=uuid.uuid4(),
        username=request.username,
        email=request.email,
    )
    service.create(user)

@router.put("/{user_id}")
def update_user(user_id: uuid.UUID, request: UpdateUserRequest):
    user = UserUpdate(
        username=request.username,
        email=request.email,
    )
    service.update(user_id, user)

@router.delete("/{user_id}")
def delete_user(user_id: uuid.UUID):
    service.delete(user_id)