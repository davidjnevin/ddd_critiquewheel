from uuid import uuid4

import pytest

from critique_wheel.members.models.IAM import MemberStatus
from critique_wheel.members.value_objects import MemberId
from critique_wheel.works.value_objects import WorkId
from tests.integration import fake_work_repository


def test_repository_can_save_a_work(
    session, valid_work, another_valid_work, active_valid_member
):
    active_valid_member.status = MemberStatus.ACTIVE
    work = valid_work
    work.member_id = active_valid_member.id
    work_2 = another_valid_work
    work_2.member_id = active_valid_member.id

    repo = fake_work_repository.FakeWorkRepository([])
    repo.add(work)
    repo.add(work_2)
    session.commit()

    assert work and work_2 in repo.list()
    assert repo.get_work_by_id(work_2.id) == work_2


@pytest.mark.current
def test_repository_can_get_a_work_by_id(session, valid_work, active_valid_member):
    work = valid_work
    repo = fake_work_repository.FakeWorkRepository(session)
    valid_work.id = WorkId.from_string(str(uuid4()))
    work.member_id = active_valid_member.id
    repo.add(work)
    session.commit()
    assert repo.get_work_by_id(work.id) == work
    assert work in repo.list()


@pytest.mark.current
def test_repository_can_get_work_by_member_id(session, valid_work, active_valid_member):
    work = valid_work
    active_valid_member.id = MemberId.from_string(str(uuid4()))
    valid_work.id = WorkId.from_string(str(uuid4()))
    work.member_id = active_valid_member.id
    repo = fake_work_repository.FakeWorkRepository(session)
    repo.add(work)
    session.commit()

    assert repo.get_work_by_member_id(work.member_id) == work
    assert work in repo.list()


@pytest.mark.current
def test_respository_returns_none_when_no_work_found(session):
    repo = fake_work_repository.FakeWorkRepository(session)
    work_id = WorkId.from_string(str(uuid4()))
    member_id = MemberId.from_string(str(uuid4()))
    assert repo.get_work_by_id(work_id) is None
    assert repo.get_work_by_member_id(member_id) is None
