from uuid import UUID
from app.repository import travel as repo
from app.service.models import Travel, TravelUpdate



def get() -> list[Travel]:
    return repo.get()

def get_by_id(id: UUID) -> Travel:
    return repo.get_by_id(id)

def create(travel: Travel):
    repo.add(travel)

def update(id: UUID, travel: TravelUpdate):
    print(travel)
    repo.update(id, travel)

def delete(id: UUID):
    repo.delete(id)