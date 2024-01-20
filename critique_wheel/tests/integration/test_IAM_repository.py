from uuid import uuid4

import pytest
from sqlalchemy import text

from critique_wheel.adapters.sqlalchemy import iam_repository
from critique_wheel.critiques.models.critique import Critique
from critique_wheel.members.models.IAM import MemberStatus
from critique_wheel.members.value_objects import MemberId
from critique_wheel.works.models.work import Work
from critique_wheel.works.value_objects import WorkId

pytestmark = pytest.mark.usefixtures("mappers")


def test_repository_can_save_a_basic_member(
    session, active_valid_member, valid_work, valid_critique
):
    member = active_valid_member
    member.id = MemberId()
    repo = iam_repository.MemberRepository(session)
    assert member.works == []
    assert member.critiques == []
    repo.add(member)
    valid_work.id = WorkId()
    valid_work.member_id = member.id

    member.works.append(valid_work)
    member.critiques.append(valid_critique)
    session.commit()

    rows = list(
        session.execute(
            text(
                "SELECT id, username, email, password, member_type, status FROM members"
            )
        )
    )
    assert rows == [
        (
            member.id.get_uuid(),
            member.username,
            member.email,
            member.password,
            member.member_type.value,
            member.status.value,
        )
    ]


def test_repository_can_get_a_member_by_id(
    session, valid_member, valid_work, valid_critique
):
    valid_member.id = MemberId()
    valid_member.status = MemberStatus.ACTIVE
    member = valid_member
    repo = iam_repository.MemberRepository(session)
    repo.add(member)
    valid_work.member_id = member.id
    valid_critique.member_id = member.id
    member.works.append(valid_work)
    member.critiques.append(valid_critique)
    assert len(member.works) == 1
    assert len(member.critiques) == 1
    session.commit()

    stmt = text('SELECT * FROM "members" WHERE id=:id').bindparams(
        id=valid_member.id.get_uuid(),
    )
    rows = session.execute(stmt).fetchall()
    assert len(rows) == 1

    retrieved_works = session.query(Work).filter_by(member_id=valid_member.id).all()
    assert len(retrieved_works) == 1
    assert retrieved_works[0].title == valid_work.title

    retrieved_critiques = session.query(Critique).filter_by(member_id=member.id).all()
    assert len(retrieved_critiques) == 1
    assert retrieved_critiques[0].critique_about == valid_critique.critique_about

    assert retrieved_works[0].member_id == member.id
    assert retrieved_critiques[0].member_id == member.id

    assert repo.get_member_by_id(member.id) == member
    assert member in repo.list()


def test_repository_can_get_a_member_by_email(session, valid_member):
    valid_member.id = MemberId()
    valid_member.status = MemberStatus.ACTIVE
    valid_member.email = "another_email@davidnevin.net"
    member = valid_member
    repo = iam_repository.MemberRepository(session)
    repo.add(member)
    session.commit()

    assert repo.get_member_by_email(member.email) == member


def test_resository_can_get_a_member_by_username(session, valid_member):
    valid_member.id = MemberId()
    valid_member.status = MemberStatus.ACTIVE
    valid_member.username = "yet_another_username"
    member = valid_member
    repo = iam_repository.MemberRepository(session)
    repo.add(member)
    session.commit()

    assert repo.get_member_by_username(member.username) == member


def test_resository_can_get_a_list_of_members(
    session, valid_member, active_valid_member
):
    member = valid_member
    member_2 = active_valid_member
    valid_member.status = MemberStatus.ACTIVE
    repo = iam_repository.MemberRepository(session)
    repo.add(member)
    repo.add(member_2)
    session.commit()

    assert member and member_2 in repo.list()


def test_repository_returns_None_for_no_member_found(session):
    repo = iam_repository.MemberRepository(session)
    username, email, id = "not_in_db", "unknown@davidnevin.net", uuid4()
    assert repo.get_member_by_username(username) is None
    assert repo.get_member_by_email(email) is None
    assert repo.get_member_by_id(id) is None
