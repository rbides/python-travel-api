from uuid import UUID
from app.repository import user as repo
from app.service.models import User, UserUpdate



def get() -> list[User]:
    return repo.get()

def get_by_id(id: UUID) -> User:
    return repo.get_by_id(id)

def create(user: User):
    repo.add(user)

def update(id: UUID, user: UserUpdate):
    repo.update(id, user)

def delete(id: UUID):
    repo.delete(id)