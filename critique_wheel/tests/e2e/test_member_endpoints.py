import logging
import uuid

import pytest
from fastapi.testclient import TestClient

from critique_wheel.entrypoints.routers import members as members_router
from critique_wheel.main import app
from tests.helpers import create_and_insert_member, override_get_db_session

logger = logging.getLogger(__name__)
pytestmark = pytest.mark.usefixtures("mappers")


app.include_router(members_router.router)
test_client = TestClient(app)
app.dependency_overrides[members_router.get_db_session] = override_get_db_session


def test_member_endpoint_returns_404_if_id_does_not_exist():
    nonexistant_member_id = uuid.uuid4()
    response = test_client.get(f"/members/{nonexistant_member_id}")
    assert response.status_code == 404


def test_create_member_endpoint_returns_member():
    payload = {
        "username": "PeterPan",
        "email": "yet_some_other_random@email.com",
        "password": "wertsdfsa12D!",
        "status": "active",
    }

    response = test_client.post("/members/", json=payload)
    logger.debug(response.json())
    assert response.status_code == 201
    assert response.json()["username"] == payload["username"]
    assert response.json()["email"] == payload["email"]
    assert response.json()["password"] != payload["password"]


def test_register_member_endpoint_returns_success_message():
    payload = {
        "username": "davidnevin",
        "email": "a_member_email@davidnevin.net",
        "password": "bhsrugh^yygTY!",
        "confirm_password": "bhsrugh^yygTY!",
    }

    response = test_client.post("/members/register/", json=payload)
    logger.debug(response.json())
    assert response.status_code == 201
    assert response.json()["detail"] == "User created. Please confirm your email"


def test_duplicate_info_register_member_endpoint_returns_DuplicateEntryError(
    sqlite_session_factory,
):
    session = sqlite_session_factory()
    _ = create_and_insert_member(session)
    session.commit()

    payload = {
        "username": "Peter Pan",
        "email": "some_random+password@davidnevin.net",
        "password": "adsfhjsdaf65rtdTTFd!",
        "confirm_password": "adsfhjsdaf65rtdTTFd!",
    }

    response = test_client.post("/members/register/", json=payload)
    logger.debug(response.json())
    assert response.status_code == 201
    assert response.json()["detail"] == "User created. Please confirm your email"
