import logging
import uuid

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from critique_wheel import config
from critique_wheel.adapters.sqlalchemy import iam_repository
from critique_wheel.entrypoints.routers.works import get_db_session
from critique_wheel.infrastructure import database as db_config
from critique_wheel.main import app
from critique_wheel.members.services import iam_service

logger = logging.getLogger(__name__)


def override_get_local_db_session():
    get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
    yield get_session


app.dependency_overrides[get_db_session] = override_get_local_db_session


@pytest.fixture
def test_client():
    with TestClient(app) as client:
        client.base_url = config.get_api_url()
        client.headers["Content-Type"] = "application/json"
        client.headers["Accept"] = "application/json"
        yield client


@pytest.mark.current
@pytest.mark.anyio
async def test_create_member_endpoint_returns_work(
    test_client: TestClient,
):
    payload = {
        "username": "PeterPan",
        "email": "some_other_random@email.com",
        "password": "wertsdfsa12D!",
        "status": "active",
    }

    response = test_client.post("/member", json=payload)
    logger.debug(response.json())
    breakpoint()
    assert response.status_code == 201
    assert response.json()["username"] == payload["username"]
    assert response.json()["email"] == payload["email"]
    assert response.json()["password"] != payload["password"]


# @pytest.mark.current
@pytest.mark.anyio
# @pytest.mark.usefixtures("postgres_db")
async def test_work_api_returns_work(
    async_client: AsyncClient,
    work_details,
):
    session = db_config.get_session_local()()
    repo = iam_repository.MemberRepository(session)
    member_id = iam_service.add_member(
        username="PeterPan",
        email="some_random@email.com",
        password="wertsdfsa12D!",
        session=session,
        repo=repo,
    )

    work_details["member_id"] = str(member_id)
    logger.debug(work_details)
    add_response = await async_client.post("/work", json=work_details)
    breakpoint()
    logger.debug(add_response.json())
    work_id = add_response.json()["id"]
    response = await async_client.get(f"/work/{work_id}")
    assert response.status_code == 200
    assert response.json()["title"] == work_details["title"]


@pytest.mark.anyio
async def test_work_api_returns_404_if_id_does_not_exist(
    async_client: AsyncClient,
):
    nonexistant_work_id = uuid.uuid4()
    response = await async_client.get(f"/work/{nonexistant_work_id}")
    assert response.status_code == 404
