from uuid import uuid4

from tests.end_to_end import fake_work_repository
from critique_wheel.domain.models.IAM import MemberStatus
from critique_wheel.infrastructure.utils.db_utils import format_uuid_for_db


def test_repository_can_save_a_work(session, valid_work, another_valid_work, active_valid_member):
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

def test_repository_can_get_a_work_by_id(session, valid_work):
    work = valid_work
    repo = fake_work_repository.FakeWorkRepository(session)
    repo.add(work)
    session.commit()
    assert repo.get_work_by_id(work.id) == work
    assert repo.list() == [work]


def test_repository_can_get_work_by_member_id(session, valid_work):
    work = valid_work
    repo = fake_work_repository.FakeWorkRepository(session)
    repo.add(work)
    session.commit()

    assert repo.get_work_by_member_id(work.member_id) == work
    assert repo.list() == [work]

def test_respository_returns_none_when_no_work_found(session):
    repo = fake_work_repository.FakeWorkRepository(session)
    id = uuid4()
    assert repo.get_work_by_id(id) is None
    assert repo.get_work_by_member_id(id) is None
