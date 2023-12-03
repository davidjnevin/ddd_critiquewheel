import pytest
import requests

from critique_wheel import config
from critique_wheel.members.value_objects import MemberId
from critique_wheel.works.models.work import Work
from critique_wheel.works.value_objects import Content, Title, WorkId


@pytest.mark.usefixtures("restart_api")
def test_work_api_returns_work(work_details, add_work):
    work = Work(
        work_id=WorkId(),
        title=Title(work_details["title"]),
        content=Content(work_details["content"]),
        age_restriction=work_details["age_restriction"],
        genre=work_details["genre"],
        member_id=MemberId(),
    )
    add_work(work)
    url = config.get_api_url()

    response = requests.get(f"{url}/works/{work.id}")
    assert response.status_code == 200
    assert response.json()["title"] == work_details["title"]
