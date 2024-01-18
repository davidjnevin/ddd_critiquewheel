import logging
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from critique_wheel.adapters.orm import mapper_registry
from critique_wheel.entrypoints.routers import members as members_router
from critique_wheel.main import app

logger = logging.getLogger(__name__)

pytestmark = pytest.mark.usefixtures("mappers")
SQLITE_DB_URI = "sqlite:///"


def override_get_db_session():
    engine = create_engine(
        SQLITE_DB_URI,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True,
    )
    logger.debug(f"Using {engine} database engine")
    mapper_registry.metadata.create_all(engine)
    try:
        db = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
        )
        yield db
    finally:
        db().close()


app.include_router(members_router.router)
test_client = TestClient(app)
app.dependency_overrides[members_router.get_db_session] = override_get_db_session


@pytest.mark.current
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


@pytest.mark.current
def test_member_endpoint_returns_404_if_id_does_not_exist():
    nonexistant_member_id = uuid.uuid4()
    response = test_client.get(f"/members/{nonexistant_member_id}")
    assert response.status_code == 404
