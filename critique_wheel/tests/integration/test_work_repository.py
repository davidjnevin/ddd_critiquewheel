import uuid

from sqlalchemy import text

from critique_wheel.adapters.sqlalchemy import work_repository
from critique_wheel.infrastructure.utils.db_utils import format_uuid_for_db



def test_repository_can_save_a_work(session, valid_work):
    work = valid_work
    repo = work_repository.SqlAlchemyWorkRepository(session)
    repo.add(work)
    session.commit()

    rows = list(session.execute(text('SELECT id, title, content, age_restriction, genre, member_id FROM "works"')))
    assert rows == [
        (
            format_uuid_for_db(work.id),
            work.title,
            work.content,
            work.age_restriction.value,
            work.genre.value,
            format_uuid_for_db(work.member_id),
        )
    ]


def test_repository_can_get_a_work_by_id(session, valid_work):
    work = valid_work
    repo = work_repository.SqlAlchemyWorkRepository(session)
    repo.add(work)
    session.commit()

    id_to_get = work.id
    stmt = text('SELECT id, title, content, age_restriction, genre, member_id FROM "works" WHERE id=:id').bindparams(
        id=id_to_get
    )
    rows = session.execute(stmt).fetchall()
    assert rows == [
        (
            format_uuid_for_db(work.id),
            work.title,
            work.content,
            work.age_restriction.value,
            work.genre.value,
            format_uuid_for_db(work.member_id),
        )
    ]
