import pytest
from sqlalchemy import text

from critique_wheel.adapters.sqlalchemy import critique_repository
from critique_wheel.critiques.value_objects import CritiqueId

pytestmark = pytest.mark.usefixtures("mappers")


def test_repository_can_save_a_critique(session, valid_critique):
    critique = valid_critique
    critique.id = CritiqueId()
    repo = critique_repository.CritiqueRepository(session)
    repo.add(critique)
    session.commit()

    rows = list(
        session.execute(
            text(
                "SELECT id, critique_about, critique_successes, critique_weaknesses, critique_ideas, member_id, work_id, status FROM critiques WHERE id=:id"
            ).bindparams(
                id=critique.id.get_uuid(),
            )
        )
    )
    assert rows == [
        (
            critique.id.get_uuid(),
            str(critique.critique_about),
            str(critique.critique_successes),
            str(critique.critique_weaknesses),
            str(critique.critique_ideas),
            critique.member_id.get_uuid(),
            critique.work_id.get_uuid(),
            critique.status.value,
        )
    ]


def test_repository_can_get_a_critique_by_id(session, valid_critique):
    critique = valid_critique
    critique.id = CritiqueId()
    repo = critique_repository.CritiqueRepository(session)
    repo.add(critique)
    session.commit()

    id_to_get = critique.id.get_uuid()
    stmt = text(
        'SELECT id, critique_about, critique_successes, critique_weaknesses, critique_ideas, member_id, work_id, status FROM "critiques" WHERE id=:id_to_get'
    ).bindparams(id_to_get=id_to_get)

    rows = session.execute(stmt).fetchall()
    assert rows == [
        (
            critique.id.get_uuid(),
            str(critique.critique_about),
            str(critique.critique_successes),
            str(critique.critique_weaknesses),
            str(critique.critique_ideas),
            critique.member_id.get_uuid(),
            critique.work_id.get_uuid(),
            critique.status.value,
        )
    ]
    assert critique == repo.get(critique.id)
    assert critique in repo.list()
