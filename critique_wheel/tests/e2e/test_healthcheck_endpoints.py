import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_healthcheck_api_returns_ok(
    async_client: AsyncClient,
):
    response = await async_client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
