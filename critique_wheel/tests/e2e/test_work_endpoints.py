import logging
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from critique_wheel.entrypoints.routers import works as works_router
from critique_wheel.main import app
from critique_wheel.works.value_objects import WorkAgeRestriction, WorkGenre, WorkStatus
from tests.helpers import create_and_insert_member, override_get_db_session

logger = logging.getLogger(__name__)
pytestmark = pytest.mark.usefixtures("mappers")


app.include_router(works_router.router)
test_client = TestClient(app)
app.dependency_overrides[works_router.get_db_session] = override_get_db_session


@pytest.mark.current
def test_work_endpoint_returns_404_if_id_does_not_exist():
    nonexistant_work_id = uuid4()
    response = test_client.get(f"/works/{nonexistant_work_id}")
    assert response.status_code == 404


@pytest.mark.current
def test_create_work_endpoint_returns_work(work_details, sqlite_session_factory):
    breakpoint()
    session = sqlite_session_factory()
    member_id = create_and_insert_member(session)
    session.commit()

    payload = {
        "title": "Test Title",
        "content": "Test content",
        "status": WorkStatus.PENDING_REVIEW,
        "age_restriction": WorkAgeRestriction.ADULT,
        "genre": WorkGenre.YOUNGADULT,
        "member_id": member_id,
    }

    response = test_client.post("/works/", json=payload)
    logger.debug(response.json())
    assert response.status_code == 201
    assert response.json()["title"] == payload["Test Title"]
