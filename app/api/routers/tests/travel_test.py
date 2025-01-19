from datetime import datetime
from uuid import UUID

import pytest
from fastapi import HTTPException, status

from app.api.routers.travel import get_travel
from app.service.errors.travel import TravelNotFoundException
from app.service.models.travel import Travel

travel_example = Travel(
    id=UUID("813bf2d2-48f1-48ee-976e-49e3f7b21e9e"),
    name="Travel package n1",
    destination="Somewhere",
    price=100.0,
    departure=datetime.now(),
)


# TODO: Should we mock the service layer
#  or the db layer as in repo (sqlalchemy.orm.Query.get) ?
def test_get_by_id_success(mocker):
    id = UUID("813bf2d2-48f1-48ee-976e-49e3f7b21e9e")
    mocker.patch(
        "app.api.routers.travel.service.get_by_id", return_value=travel_example
    )
    travel = get_travel(id)
    assert travel.id == id
    assert isinstance(travel, Travel)


def test_get_by_id_not_found(mocker):
    id = "813bf2d2-48f1-48ee-976e-49e3f7b21e9e"
    mocker.patch(
        "app.api.routers.travel.service.get_by_id",
        side_effect=TravelNotFoundException(),
    )
    with pytest.raises(HTTPException) as e:
        get_travel(id)
    assert e.value.status_code == status.HTTP_404_NOT_FOUND
    assert e.value.detail == "Travel not found."
    assert e.type is HTTPException
