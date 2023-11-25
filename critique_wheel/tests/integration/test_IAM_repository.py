from uuid import uuid4

from sqlalchemy import text

from critique_wheel.adapters.sqlalchemy import iam_repository
from critique_wheel.domain.models.critique import Critique
from critique_wheel.domain.models.IAM import MemberStatus
from critique_wheel.domain.models.work import Work


def test_repository_can_save_a_basic_member(
    session, active_valid_member, valid_work, valid_critique
):
    member = active_valid_member
    repo = iam_repository.SqlAlchemyMemberRepository(session)
    assert member.works == []
    assert member.critiques == []
    repo.add(member)
    member.add_work(valid_work)
    member.add_critique(valid_critique)
    session.commit()

    rows = list(
        session.execute(
            text(
                'SELECT id, username, email, password, member_type, status FROM "members"'
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
    member = valid_member
    valid_member.status = MemberStatus.ACTIVE
    repo = iam_repository.SqlAlchemyMemberRepository(session)
    repo.add(member)
    valid_work.member_id = member.id
    valid_critique.member_id = member.id
    member.add_work(valid_work)
    member.add_critique(valid_critique)
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

    retrieved_critiques = (
        session.query(Critique).filter_by(member_id=valid_member.id).all()
    )
    assert len(retrieved_critiques) == 1
    assert retrieved_critiques[0].critique_about == valid_critique.critique_about

    assert retrieved_works[0].member_id == valid_member.id
    assert retrieved_critiques[0].member_id == valid_member.id

    assert repo.get_member_by_id(valid_member.id) == valid_member
    assert repo.list() == [valid_member]


def test_resository_can_get_a_member_by_email(session, valid_member):
    member = valid_member
    valid_member.status = MemberStatus.ACTIVE
    repo = iam_repository.SqlAlchemyMemberRepository(session)
    repo.add(member)
    session.commit()

    assert repo.get_member_by_email(valid_member.email) == valid_member


def test_resository_can_get_a_member_by_username(session, valid_member):
    member = valid_member
    valid_member.status = MemberStatus.ACTIVE
    repo = iam_repository.SqlAlchemyMemberRepository(session)
    repo.add(member)
    session.commit()

    assert repo.get_member_by_username(valid_member.username) == valid_member


def test_resository_can_get_a_list_of_members(
    session, valid_member, active_valid_member
):
    member = valid_member
    member_2 = active_valid_member
    valid_member.status = MemberStatus.ACTIVE
    repo = iam_repository.SqlAlchemyMemberRepository(session)
    repo.add(member)
    repo.add(member_2)
    session.commit()

    assert member and member_2 in repo.list()


def test_repository_returns_None_for_no_member_found(session):
    repo = iam_repository.SqlAlchemyMemberRepository(session)
    username, email, id = "not_in_db", "unknown@davidnevin.net", uuid4()
    assert repo.get_member_by_username(username) is None
    assert repo.get_member_by_email(email) is None
    assert repo.get_member_by_id(id) is None
