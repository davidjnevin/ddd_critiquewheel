import logging
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from critique_wheel.adapters import orm
from critique_wheel.entrypoints.routers.works import get_db_session
from critique_wheel.infrastructure import database as db_config
from critique_wheel.main import app

logger = logging.getLogger(__name__)

engine = create_engine(db_config.get_postgres_uri())


def override_get_local_db_session():
    try:
        orm.MapperRegistry.start_mappers()
        local_db_session = sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=False,
        )
        db = local_db_session
        yield db
    finally:
        db.close()


breakpoint()
app.dependency_overrides[get_db_session] = override_get_local_db_session
test_client = TestClient(app)


@pytest.mark.current
def test_create_member_endpoint_returns_member():
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


@pytest.mark.current
def test_member_endpoint_returns_404_if_id_does_not_exist():
    nonexistant_member_id = uuid.uuid4()
    response = test_client.get(f"/work/{nonexistant_member_id}")
    assert response.status_code == 404
