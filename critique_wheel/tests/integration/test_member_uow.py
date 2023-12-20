import pytest
import sqlalchemy

from critique_wheel.members.services.unit_of_work import IAMUnitOfWork
from tests.integration.fake_iam_repository import FakeMemberRepository


def insert_member(session, **kwargs):
    stmt = sqlalchemy.text(
        """
        INSERT INTO members (id, username, email, password)
        VALUES (:id, :username, :email, :password)
        """
    )
    params = kwargs
    session.execute(stmt, params)


def get_member_by_id(session, member_id):
    stmt = sqlalchemy.text(
        """
        SELECT id, username, email, password
        FROM members
        WHERE id = :id
        """
    )
    params = {
        "id": member_id,
    }
    result = session.execute(stmt, params)
    row = result.fetchone()
    if row:
        return row._mapping
    else:
        return None


class FakeUnitOfWork:
    def __init__(self):
        self.members = FakeMemberRepository([])
        self.committed = False

    def commit(self):
        self.committed = True


@pytest.mark.current
def test_uow_can_create_and_retrieve_members(session_factory, valid_member):
    uow = IAMUnitOfWork(session_factory)
    with uow:
        uow.members.add(valid_member)
        uow.commit()

    new_session = session_factory()
    member = get_member_by_id(new_session, str(valid_member.id))
    assert str(valid_member.id) == member["id"]