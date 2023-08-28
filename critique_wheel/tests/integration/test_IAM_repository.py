import pytest
from sqlalchemy import String, Uuid, text, bindparam

from critique_wheel.adapters.sqlalchemy import iam_repository
from critique_wheel.domain.models.IAM import MemberStatus
from critique_wheel.domain.models.work import Work
from critique_wheel.domain.models.critique import Critique
from critique_wheel.infrastructure.utils import db_utils


@pytest.mark.current
def test_repository_can_save_a_basic_member(session, active_valid_member, valid_work, valid_critique):
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
            db_utils.format_uuid_for_db(member.id),
            member.username,
            member.email,
            member.password,
            member.member_type.value,
            member.status.value,
        )
    ]


def test_repository_can_get_a_member_by_id(session, valid_member, valid_work, valid_critique):
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

    stmt = (
        text(
            'SELECT * FROM "members" WHERE id=:member_id'
            # 'SELECT id, username, email, password, member_type, status, works, critiques FROM "members" WHERE id=:id'
        )).bindparams(
            bindparam("member_id", type_=Uuid),
        ).bindparams(
            member_id=valid_member.id,
        )
    rows = session.execute(stmt).fetchall()
    assert len(rows) == 1


    retrieved_works = session.query(Work).filter_by(member_id=valid_member.id).all()
    assert len(retrieved_works) == 1
    assert retrieved_works[0].title == valid_work.title

    retrieved_critiques = session.query(Critique).filter_by(member_id=valid_member.id).all()
    assert len(retrieved_critiques) == 1
    assert retrieved_critiques[0].content_about == valid_critique.content_about

    assert retrieved_works[0].member_id == valid_member.id
    assert retrieved_critiques[0].member_id == valid_member.id


