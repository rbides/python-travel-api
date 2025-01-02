from datetime import datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, PlainSerializer, TypeAdapter
from sqlalchemy import  update as sql_update
from app.database.models import TravelEntity
from app.database import Session
from app.service.errors import TravelNotFoundException
from app.service.models import Travel, TravelUpdate, TravelFilters


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



class SQLFilters(BaseModel):
    name: Annotated[str | None, PlainSerializer(lambda x: TravelEntity.name.contains(x))] = None
    min_price: Annotated[Decimal | None, PlainSerializer(lambda x: TravelEntity.price >= x)] = None
    max_price: Annotated[Decimal | None, PlainSerializer(lambda x: TravelEntity.price <= x)] = None
    min_departure: Annotated[datetime | None, PlainSerializer(lambda x: TravelEntity.departure >= x)] = None
    max_departure: Annotated[datetime | None, PlainSerializer(lambda x: TravelEntity.departure <= x)] = None    

    
def get(filters: TravelFilters) -> list[Travel]:
    sql_filters = SQLFilters(**filters.model_dump(exclude_none=True, exclude="order_by"))
    with Session() as session:
        query = session.query(TravelEntity)
        for f in sql_filters.model_dump(exclude_none=True).values():
            query = query.filter(f)
        travels = query.order_by(filters.order_by).all()
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
