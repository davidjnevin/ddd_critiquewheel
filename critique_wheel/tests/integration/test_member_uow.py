from uuid import uuid4

import pytest
import sqlalchemy

from critique_wheel.members.models.IAM import MemberRole, MemberStatus
from critique_wheel.members.services.unit_of_work import IAMUnitOfWork

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


def test_uow_can_retrieve_a_member_and_alter_it(sqlite_session_factory):
    session = sqlite_session_factory()
    session.expire_on_commit = False
    id = str(uuid4())
    insert_member(
        session,
        id=id,
        username="test_username",
        password="secure_unguessab1e_p@ssword",
        email="email_address@davidneivn.net",
        member_type=MemberRole.MEMBER,
        status=MemberStatus.ACTIVE,
        works=None,
        critiques=None,
    )
    session.commit()

    uow = IAMUnitOfWork(sqlite_session_factory)
    with uow:
        member = uow.members.get_member_by_username("test_username")
        member.username = "new_username"
        uow.commit()

    member = get_member_by_id(session, id)
    assert member.username == "new_username"


@pytest.mark.current
def test_roll_back_uncommited_changes_by_default(sqlite_session_factory):
    session = sqlite_session_factory()
    session.expire_on_commit = False
    id = str(uuid4())
    insert_member(
        session,
        id=id,
        username="test_username",
        password="secure_unguessab1e_p@ssword",
        email="some_random@davidnevin.net",
        member_type=MemberRole.MEMBER,
        status=MemberStatus.ACTIVE,
        works=None,
        critiques=None,
    )
    session.commit()

    uow = IAMUnitOfWork(sqlite_session_factory)
    with uow:
        member = uow.members.get_member_by_username("test_username")
        member.username = "new_username"

    member = get_member_by_id(session, id)
    assert member.username == "test_username"


@pytest.mark.current
def test_rolls_back_on_errors(sqlite_session_factory):
    session = sqlite_session_factory()
    session.expire_on_commit = False
    id = str(uuid4())
    insert_member(
        session,
        id=id,
        username="test_username",
        password="secure_unguessab1e_p@ssword",
        email="some_random@davidnevin.net",
        member_type=MemberRole.MEMBER,
        status=MemberStatus.ACTIVE,
        works=None,
        critiques=None,
    )
    session.commit()

    uow = IAMUnitOfWork(sqlite_session_factory)
    with pytest.raises(ValueError):
        with uow:
            member = uow.members.get_member_by_username("test_username")
            member.username = "new_username"
            raise ValueError()

    member = get_member_by_id(session, id)
    assert member.username == "test_username"
