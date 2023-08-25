from sqlalchemy import text

from critique_wheel.adapters.sqlalchemy import iam_repository
from critique_wheel.infrastructure.utils.db_utils import format_uuid_for_db


def test_repository_can_save_a_member(session, valid_member):
    member = valid_member
    repo = iam_repository.SqlAlchemyMemberRepository(session)
    repo.add(member)
    session.commit()

    rows = list(session.execute(text(
        'SELECT id, username, email, password, member_type, status FROM "members"'
    )))
    assert rows == [
        (
            format_uuid_for_db(member.id),
            member.username,
            member.email,
            member.password,
            member.member_type.value,
            member.status.value,
        )
    ]


def test_repository_can_get_a_member_by_id(session, valid_member):
    member = valid_member
    repo = iam_repository.SqlAlchemyMemberRepository(session)
    repo.add(member)
    session.commit()

    id_to_get = member.id
    stmt = text(
        'SELECT id, username, email, password, member_type, status FROM "members" WHERE id=:id'
    ).bindparams(
        id=id_to_get
    )
    rows = session.execute(stmt).fetchall()
    assert rows == [
        (
            format_uuid_for_db(member.id),
            member.username,
            member.email,
            member.password,
            member.member_type.value,
            member.status.value,
        )
    ]

