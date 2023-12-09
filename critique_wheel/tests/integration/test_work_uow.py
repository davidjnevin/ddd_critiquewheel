from uuid import uuid4

import sqlalchemy

from critique_wheel.works.services.unit_of_work import SqlAlchemyUnitOfWork
from tests.integration.fake_work_repository import FakeWorkRepository


def insert_member(session, **kwargs):
    stmt = sqlalchemy.text(
        """
        INSERT INTO members (id, username, email, password)
        VALUES (:id, :username, :email, :password)
        """
    )
    params = kwargs
    session.execute(stmt, params)


def insert_work(session, **kwargs):
    stmt = sqlalchemy.text(
        """
        INSERT INTO works (id, title, content, age_restriction, genre, member_id)
        VALUES (:id, :title, :content, :age_restriction, :genre, :member_id)
        """
    )
    params = kwargs
    session.execute(stmt, params)


def get_work_by_id(session, work_id):
    stmt = sqlalchemy.text(
        """
        SELECT id, title, content, age_restriction, genre, member_id
        FROM works
        WHERE id = :id
        """
    )
    params = {
        "id": work_id,
    }
    result = session.execute(stmt, params)
    row = result.fetchone()
    if row:
        return dict(row)
    else:
        return None


class FakeUnitOfWork:
    def __init__(self):
        self.works = FakeWorkRepository([])
        self.committed = False

    def commit(self):
        self.committed = True


# @pytest.mark.current
def test_uow_can_create_and_retrieve_works(session_factory, valid_work, member_details):
    session = session_factory()
    member_details["id"] = str(uuid4())
    valid_work.id = member_details["id"]
    insert_member(
        session, **member_details
    )  # We need a member in the database to create a work
    session.commit()

    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        uow.works.add(valid_work)
        uow.commit()

    new_session = session_factory()
    work = get_work_by_id(new_session, valid_work.id)
    assert valid_work.id == work["id"]
