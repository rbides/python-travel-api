from datetime import datetime
import uuid
from fastapi import APIRouter, HTTPException, status
from app.api.models.travel import CreateTravelRequest, UpdateTravelRequest
from app.service import travel as service
from app.service.errors.travel import TravelNotFoundException
from app.service.models import Travel, TravelUpdate


router = APIRouter(
    prefix="/travels",
)


@router.get("", status_code=status.HTTP_200_OK)
def get_travels() -> list[Travel]:
    return service.get()


@router.get("/{travel_id}", status_code=status.HTTP_200_OK)
def get_travel(travel_id: uuid.UUID) -> Travel:
    try:
        return service.get_by_id(travel_id)
    except TravelNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_travel(request: CreateTravelRequest):
    travel = Travel(
        id=uuid.uuid4(),
        name=request.name,
        destination=request.destination,
        price=request.price,
        departure=request.departure,
    )
    service.create(travel)

@router.put("/{travel_id}", status_code=status.HTTP_200_OK)
def update_travel(travel_id: uuid.UUID, request: UpdateTravelRequest):
    travel = TravelUpdate(
        name=request.name,
        destination=request.destination,
        price=request.price,
        departure=request.departure,
    )
    try:
        service.update(travel_id, travel)
    except TravelNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)

@router.delete("/{travel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_travel(travel_id: uuid.UUID):
    try:
        service.delete(travel_id)
    except TravelNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)