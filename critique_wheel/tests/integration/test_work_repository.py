from uuid import uuid4

from sqlalchemy import text

from critique_wheel.adapters.sqlalchemy import work_repository
from critique_wheel.domain.models.IAM import MemberStatus


def test_repository_can_save_a_work(
    session, valid_work, another_valid_work, active_valid_member
):
    active_valid_member.status = MemberStatus.ACTIVE
    work = valid_work
    work.member_id = active_valid_member.id
    work_2 = another_valid_work
    work_2.member_id = active_valid_member.id
    repo = work_repository.SqlAlchemyWorkRepository(session)
    repo.add(work)
    repo.add(work_2)
    session.commit()

    rows = list(
        session.execute(
            text(
                'SELECT id, title, content, age_restriction, genre, member_id FROM "works"'
            )
        )
    )
    assert rows == [
        (
            work.id.get_uuid(),
            str(work.title),
            str(work.content),
            work.age_restriction.value,
            work.genre.value,
            work.member_id.get_uuid(),
        ),
        (
            work_2.id.get_uuid(),
            str(work_2.title),
            str(work_2.content),
            work_2.age_restriction.value,
            work_2.genre.value,
            work.member_id.get_uuid(),
        ),
    ]


def test_repository_can_get_a_work_by_id(session, valid_work):
    work = valid_work
    repo = work_repository.SqlAlchemyWorkRepository(session)
    repo.add(work)
    session.commit()

    id_to_get = work.id
    stmt = text(
        'SELECT id, title, content, age_restriction, genre, member_id FROM "works" WHERE id=:id'
    ).bindparams(id=work.id.get_uuid())
    rows = session.execute(stmt).fetchall()
    assert rows == [
        (
            work.id.get_uuid(),
            str(work.title),
            str(work.content),
            work.age_restriction.value,
            work.genre.value,
            work.member_id.get_uuid(),
        )
    ]

    assert repo.get_work_by_id(id_to_get) == work
    assert repo.list() == [work]


def test_repository_can_get_work_by_member_id(session, valid_work):
    work = valid_work
    repo = work_repository.SqlAlchemyWorkRepository(session)
    repo.add(work)
    session.commit()

    member_id_to_get = str(work.member_id)
    stmt = text(
        'SELECT id, title, content, age_restriction, genre, member_id FROM "works" WHERE member_id=:member_id'
    ).bindparams(member_id=member_id_to_get)
    rows = session.execute(stmt).fetchall()
    assert rows == [
        (
            work.id.get_uuid(),
            str(work.title),
            str(work.content),
            work.age_restriction.value,
            work.genre.value,
            work.member_id.get_uuid(),
        )
    ]

    assert repo.get_work_by_member_id(member_id_to_get) == work
    assert repo.list() == [work]


def test_respository_returns_none_when_no_work_found(session):
    repo = work_repository.SqlAlchemyWorkRepository(session)
    id = uuid4()
    assert repo.get_work_by_id(id) is None
    assert repo.get_work_by_member_id(id) is None
