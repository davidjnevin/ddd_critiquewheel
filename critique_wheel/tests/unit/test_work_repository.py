from sqlalchemy import text

from critique_wheel.adapters.sqlalchemy import work_repository


def test_repository_can_save_a_work(session, valid_work):
    work = valid_work
    repo = work_repository.SqlAlchemyWorkRepository(session)
    repo.add(work)
    session.commit()

    rows = list(session.execute(text('SELECT title, content, age_restriction, genre FROM "works"')))
    assert rows == [(work.title, work.content, work.age_restriction.value.upper(), work.genre.value.upper())]


def test_repository_can_get_a_work(session, valid_work):
    work = valid_work
    repo = work_repository.SqlAlchemyWorkRepository(session)
    repo.add(work)
    session.commit()

    id_to_get = work.id
    stmt = text('SELECT title, content, age_restriction, genre FROM "works" WHERE id=:id').bindparams(id=id_to_get)
    rows = session.execute(stmt).fetchall()
    assert rows == [(work.title, work.content, work.age_restriction.value.upper(), work.genre.value.upper())]
