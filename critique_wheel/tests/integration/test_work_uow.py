from uuid import uuid4

import pytest
import sqlalchemy

from critique_wheel.works.services.unit_of_work import WorkUnitOfWork

pytestmark = pytest.mark.usefixtures("mappers")


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


def get_work_by_member_id(session, member_id):
    stmt = sqlalchemy.text(
        """
        SELECT id, title, content, age_restriction, genre, member_id
        FROM works
        WHERE member_id = :member_id
        """
    )
    params = {
        "member_id": member_id,
    }
    result = session.execute(stmt, params)
    row = result.fetchone()
    if row:
        return row._mapping
    else:
        return None


def test_uow_can_create_and_retrieve_works(
    sqlite_session_factory, valid_work, member_details
):
    session = sqlite_session_factory()
    id = str(uuid4())
    member_details["id"] = id
    insert_member(
        session, **member_details
    )  # We need a member in the database to create a work
    session.commit()

    valid_work.member_id = member_details["id"]
    uow = WorkUnitOfWork(sqlite_session_factory)
    with uow:
        uow.works.add(valid_work)
        uow.commit()

    new_session = sqlite_session_factory()
    work = get_work_by_member_id(new_session, id)
    assert id == work["member_id"]
    assert "Test Title" == work["title"]
