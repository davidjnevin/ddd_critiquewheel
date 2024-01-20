import pytest
from fastapi.testclient import TestClient

from critique_wheel.main import app

client = TestClient(app)


@pytest.mark.anyio
def test_healthcheck_api_returns_ok():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
