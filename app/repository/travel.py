from uuid import UUID

from pydantic import TypeAdapter
from sqlalchemy import update as sql_update
from app.database.models import TravelEntity
from app.database import Session
from app.service.errors import TravelNotFoundException
from app.service.models import Travel, TravelUpdate


def add(travel: Travel):
    with Session.begin() as session:
        session.add(TravelEntity(**travel.model_dump()))

def update(id: UUID, travel: TravelUpdate):
    with Session.begin() as session:
        query = session.execute(
            sql_update(TravelEntity)
                .where(TravelEntity.id==id)
                .values(travel.model_dump(exclude_none=True))
        )
        if query.rowcount == 0:
            raise TravelNotFoundException()

def get() -> list[Travel]:
    with Session() as session:
        travels = session.query(TravelEntity).all()
    ta = TypeAdapter(list[Travel])
    return ta.validate_python(travels)

def get_by_id(id: UUID) -> Travel:
    with Session() as session:
        travel = session.query(TravelEntity).get(id)
    if travel is None:
        raise TravelNotFoundException()
    return Travel.model_validate(travel)

def delete(id: UUID):
    with Session.begin() as session:
        travel = session.query(TravelEntity).get(id)
        if travel is None:
            raise TravelNotFoundException()
        session.delete(travel)
