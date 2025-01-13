from uuid import UUID

from app.repository import travel as repo
from app.service.models.travel import Travel, TravelFilters, TravelUpdate

# TODO: Put the logs here in the service layer


def get(filters: TravelFilters) -> list[Travel]:
    return repo.get(filters)


def get_by_id(id: UUID) -> Travel:
    return repo.get_by_id(id)


def create(travel: Travel):
    repo.add(travel)


def update(id: UUID, travel: TravelUpdate):
    print(travel)
    repo.update(id, travel)


def delete(id: UUID):
    repo.delete(id)
