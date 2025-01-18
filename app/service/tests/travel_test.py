from datetime import datetime
from uuid import UUID

import pytest

from app.service.errors.travel import TravelNotFoundException
from app.service.models.travel import Travel
from app.service.travel import get_by_id

travel_example = Travel(
    id=UUID("813bf2d2-48f1-48ee-976e-49e3f7b21e9e"),
    name="Travel package n1",
    destination="Somewhere",
    price=100.0,
    departure=datetime.now(),
)


def test_get_by_id_success(mocker):
    id = UUID("813bf2d2-48f1-48ee-976e-49e3f7b21e9e")
    mocker.patch(
        "app.service.travel.repo.get_by_id", return_value=travel_example
    )
    travel = get_by_id(id)
    assert travel.id == id
    assert isinstance(travel, Travel)


def test_get_by_id_not_found(mocker):
    id = "813bf2d2-48f1-48ee-976e-49e3f7b21e9e"
    mocker.patch(
        "app.service.travel.repo.get_by_id",
        side_effect=TravelNotFoundException(),
    )
    with pytest.raises(TravelNotFoundException):
        get_by_id(id)
