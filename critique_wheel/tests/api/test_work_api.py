import pytest
from httpx import AsyncClient

from critique_wheel.members.value_objects import MemberId
from critique_wheel.works.models.work import Work
from critique_wheel.works.value_objects import Content, Title, WorkId


@pytest.mark.anyio
async def test_work_api_returns_work(
    async_client: AsyncClient,
    work_details,
    add_work,
):
    work = Work(
        work_id=WorkId(),
        title=Title(work_details["title"]),
        content=Content(work_details["content"]),
        age_restriction=work_details["age_restriction"],
        genre=work_details["genre"],
        member_id=MemberId(),
    )
    add_work(work)
    response = await async_client.get(f"/works/{work.id}")
    assert response.status_code == 200
    assert response.json()["title"]["value"] == work_details["title"]
