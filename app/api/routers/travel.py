import uuid
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query, Security, status

from app.api.models.travel import CreateTravelRequest, UpdateTravelRequest
from app.service import auth
from app.service import travel as service
from app.service.errors.travel import TravelNotFoundException
from app.service.models.travel import Travel, TravelFilters, TravelUpdate
from app.utils.enums import Permissions

router = APIRouter(
    prefix="/travels",
)

# Using Annotated only on api layer so
# we have proper documentation for external consumers.


@router.get("", status_code=status.HTTP_200_OK)
def get_travels(
    query_params: Annotated[TravelFilters, Query(title="Filter options")]
) -> list[Travel]:
    return service.get(query_params)


@router.get("/{travel_id}", status_code=status.HTTP_200_OK)
def get_travel(
    travel_id: Annotated[uuid.UUID, Path(title="The id of the travel to get")]
) -> Travel:
    try:
        return service.get_by_id(travel_id)
    except TravelNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.detail
        )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Security(
            auth.verify_permissions, scopes=[Permissions.TRAVEL_WRITE.value]
        )
    ],
)
def create_travel(request: CreateTravelRequest):
    travel = Travel(
        id=uuid.uuid4(),
        name=request.name,
        destination=request.destination,
        price=request.price,
        departure=request.departure,
    )
    service.create(travel)


@router.put(
    "/{travel_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[
        Security(
            auth.verify_permissions, scopes=[Permissions.TRAVEL_WRITE.value]
        )
    ],
)
def update_travel(
    travel_id: Annotated[
        uuid.UUID, Path(title="The id of the travel to update")
    ],
    request: UpdateTravelRequest,
):
    travel = TravelUpdate(
        name=request.name,
        destination=request.destination,
        price=request.price,
        departure=request.departure,
    )
    try:
        service.update(travel_id, travel)
    except TravelNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.detail
        )


@router.delete(
    "/{travel_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Security(
            auth.verify_permissions, scopes=[Permissions.TRAVEL_DELETE.value]
        )
    ],
)
def delete_travel(
    travel_id: Annotated[
        uuid.UUID, Path(title="The id of the travel to delete")
    ]
):
    try:
        service.delete(travel_id)
    except TravelNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.detail
        )
