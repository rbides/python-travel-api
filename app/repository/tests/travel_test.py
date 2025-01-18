from datetime import datetime
from uuid import UUID

import pytest

from app.database.models.travel import TravelEntity
from app.repository.travel import get_by_id
from app.service.errors.travel import TravelNotFoundException
from app.service.models.travel import Travel

travel_example = Travel(
    id=UUID("813bf2d2-48f1-48ee-976e-49e3f7b21e9e"),
    name="Travel package n1",
    destination="Somewhere",
    price=100.0,
    departure=datetime.now(),
)

travel_entity_example = TravelEntity(**travel_example.model_dump())


def test_get_by_id_success(mocker):
    id = UUID("813bf2d2-48f1-48ee-976e-49e3f7b21e9e")
    mocker.patch(
        "sqlalchemy.orm.Query.get", return_value=travel_entity_example
    )
    travel = get_by_id(id)
    assert travel.id == id
    assert isinstance(travel, Travel)


def test_get_by_id_not_found(mocker):
    id = "813bf2d2-48f1-48ee-976e-49e3f7b21e9e"
    mocker.patch("sqlalchemy.orm.Query.get", return_value=None)
    with pytest.raises(TravelNotFoundException):
        get_by_id(id)
