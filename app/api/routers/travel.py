from datetime import datetime
import uuid
from fastapi import APIRouter
from app.api.models.travel import CreateTravelRequest, UpdateTravelRequest
from app.service import travel as service
from app.service.models import Travel, TravelUpdate


router = APIRouter(
    prefix="/travels",
)


@router.get("")
def get_travels():
    return service.get()


@router.get("/{travel_id}")
def get_travel(travel_id: uuid.UUID):
    return service.get_by_id(travel_id)


@router.post("")
def create_travel(request: CreateTravelRequest):
    travel = Travel(
        id=uuid.uuid4(),
        name=request.name,
        destination=request.destination,
        price=request.price,
        departure=request.departure,
    )
    service.create(travel)

@router.put("/{travel_id}")
def update_travel(travel_id: uuid.UUID, request: UpdateTravelRequest):
    travel = TravelUpdate(
        name=request.name,
        destination=request.destination,
        price=request.price,
        departure=request.departure,
    )
    service.update(travel_id, travel)

@router.delete("/{travel_id}")
def delete_travel(travel_id: uuid.UUID):
    service.delete(travel_id)