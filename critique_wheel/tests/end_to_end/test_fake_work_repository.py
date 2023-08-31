from uuid import uuid4

import pytest

from critique_wheel.domain.models.IAM import MemberStatus, MemberRole
from tests.end_to_end.fake_iam_repository import FakeMemberRepository


def test_repository_can_save_a_basic_member(session, active_valid_member, valid_work, valid_critique):
    member = active_valid_member
    repo = FakeMemberRepository(session)
    assert member.works == []
    assert member.critiques == []
    member.add_work(valid_work)
    member.add_critique(valid_critique)
    repo.add(member)
    session.commit()

    assert member.id is not None
    assert member.username == "test_username"
    assert member.password != "secure_unguessable_p@ssword"
    assert member.email == "email_address@davidneivn.net"
    assert member.member_type == MemberRole.MEMBER
    assert member.status == MemberStatus.ACTIVE
    assert member.works != None
    assert member.critiques != None


def test_repository_can_get_a_member_by_id(session, valid_member, valid_work, valid_critique):
    member = valid_member
    valid_member.status = MemberStatus.ACTIVE
    repo = FakeMemberRepository(session)
    valid_work.member_id = member.id
    valid_critique.member_id = member.id
    member.add_work(valid_work)
    member.add_critique(valid_critique)
    assert len(member.works) == 1
    assert len(member.critiques) == 1
    repo.add(member)
    session.commit()

    assert repo.get_member_by_id(valid_member.id) == valid_member
    assert repo.list() == [valid_member]


def test_resository_can_get_a_member_by_email(session, valid_member):
    member = valid_member
    valid_member.status = MemberStatus.ACTIVE
    repo = FakeMemberRepository(session)
    repo.add(member)
    session.commit()

    assert repo.get_member_by_email(valid_member.email) == valid_member


def test_resository_can_get_a_member_by_username(session, valid_member):
    member = valid_member
    valid_member.status = MemberStatus.ACTIVE
    repo = FakeMemberRepository(session)
    repo.add(member)
    session.commit()

    assert repo.get_member_by_username(valid_member.username) == valid_member


def test_resository_can_get_a_list_of_members(session, valid_member, active_valid_member):
    member = valid_member
    member_2 = active_valid_member
    valid_member.status = MemberStatus.ACTIVE
    repo = FakeMemberRepository(session)
    repo.add(member)
    repo.add(member_2)
    session.commit()

    assert member and member_2 in repo.list()


def test_repository_returns_None_for_no_member_found(session, valid_member):
    repo = FakeMemberRepository(session)
    username, email, id = "not_in_db", "unknown@davidnevin.net", uuid4()
    assert repo.get_member_by_username(username) is None
    assert repo.get_member_by_email(email) is None
    assert repo.get_member_by_id(id) is None
