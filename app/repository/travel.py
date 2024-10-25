from uuid import UUID

from sqlalchemy import update as sql_update
from app.database.models import TravelEntity
from app.database import Session
from app.service.models import Travel, TravelUpdate


def add(travel: Travel):
    with Session.begin() as session:
        session.add(TravelEntity(**travel.model_dump()))

def update(id: UUID, travel: TravelUpdate):
    with Session.begin() as session:
        session.execute(
            sql_update(TravelEntity)
                .where(TravelEntity.id==id)
                .values(travel.model_dump(exclude_none=True))
        )

def get() -> list[TravelEntity]:
    with Session() as session:
        travels = session.query(TravelEntity).all()
    return travels

def get_by_id(id: UUID) -> TravelEntity:
    with Session() as session:
        travel = session.query(TravelEntity).get(id)
    return travel

def delete(id: UUID):
    with Session.begin() as session:
        travel = session.query(TravelEntity).get(id)
        session.delete(travel)
