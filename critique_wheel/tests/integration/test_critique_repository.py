from sqlalchemy import text

from critique_wheel.adapters.sqlalchemy import critique_repository
from critique_wheel.infrastructure.utils.db_utils import format_uuid_for_db


def test_repository_can_save_a_critique(session, valid_critique):
    critique = valid_critique
    repo = critique_repository.SqlAlchemyCritiqueRepository(session)
    repo.add(critique)
    session.commit()

    rows = list(
        session.execute(
            text(
                'SELECT id, content_about, content_successes, content_weaknesses, content_ideas, member_id, work_id, status FROM "critiques"'
            )
        )
    )
    assert rows == [
        (
            format_uuid_for_db(critique.id),
            critique.content_about,
            critique.content_successes,
            critique.content_weaknesses,
            critique.content_ideas,
            format_uuid_for_db(critique.member_id),
            format_uuid_for_db(critique.work_id),
            critique.status.value,
        )
    ]


def test_repository_can_get_a_work_by_id(session, valid_critique):
    critique = valid_critique
    repo = critique_repository.SqlAlchemyCritiqueRepository(session)
    repo.add(critique)
    session.commit()

    id_to_get = critique.id
    stmt = text(
        'SELECT id, content_about, content_successes, content_weaknesses, content_ideas, member_id, work_id, status FROM "critiques" WHERE id=:id_to_get'
    ).bindparams(id_to_get=id_to_get)

    rows = session.execute(stmt).fetchall()
    assert rows == [
        (
            format_uuid_for_db(critique.id),
            critique.content_about,
            critique.content_successes,
            critique.content_weaknesses,
            critique.content_ideas,
            format_uuid_for_db(critique.member_id),
            format_uuid_for_db(critique.work_id),
            critique.status.value,
        )
    ]
    assert critique == repo.get(critique.id)
    assert repo.list() == [critique]
