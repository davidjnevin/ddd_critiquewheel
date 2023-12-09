import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from critique_wheel.adapters.sqlalchemy import iam_repository
from critique_wheel.config import get_postgres_uri
from critique_wheel.members.services import iam_service


def get_db_session():
    get_session = sessionmaker(bind=create_engine(get_postgres_uri()))
    return get_session()


@pytest.mark.anyio
@pytest.mark.usefixtures("postgres_db")
async def test_create_work_endpoint_returns_work(
    async_client: AsyncClient,
    work_details,
):
    session = get_db_session()
    repo = iam_repository.SqlAlchemyMemberRepository(session)
    member_id = iam_service.create_member(
        username="PeterPan",
        email="some_random@email.com",
        password="wertsdfsa12D!",
        session=session,
        repo=repo,
    )

    work_details["member_id"] = str(member_id)

    response = await async_client.post("/work", json=work_details)
    assert response.status_code == 201
    assert response.json()["title"] == work_details["title"]
    assert response.json()["content"] == work_details["content"]
    assert response.json()["age_restriction"] == work_details["age_restriction"]
    assert response.json()["genre"] == work_details["genre"]
    assert response.json()["member_id"] == work_details["member_id"]
    assert response.json()["critiques"] == []


@pytest.mark.anyio
@pytest.mark.usefixtures("postgres_db")
async def test_work_api_returns_work(
    async_client: AsyncClient,
    work_details,
):
    session = get_db_session()
    repo = iam_repository.SqlAlchemyMemberRepository(session)
    member_id = iam_service.create_member(
        username="PeterPan",
        email="some_random@email.com",
        password="wertsdfsa12D!",
        session=session,
        repo=repo,
    )

    work_details["member_id"] = str(member_id)

    add_response = await async_client.post("/work", json=work_details)

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
