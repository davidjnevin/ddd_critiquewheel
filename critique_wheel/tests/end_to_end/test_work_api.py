import pytest

from critique_wheel.members.value_objects import MemberId
from critique_wheel.works.value_objects import Content, Title


@pytest.mark.current
@pytest.mark.usefixtures("restart_api")
def test_work_api_returns_work(work_service, work_details):
    work = work_service.add_work(
        title=Title(work_details["title"]),
        content=Content(work_details["content"]),
        age_restriction=work_details["age_restriction"],
        genre=work_details["genre"],
        member_id=MemberId(),
    )
    assert work == "test work"
