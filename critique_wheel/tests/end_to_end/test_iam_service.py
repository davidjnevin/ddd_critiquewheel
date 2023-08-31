from typing import Optional

import pytest
from sqlalchemy import UUID

from critique_wheel.domain.models.IAM import Member, MemberRole, MemberStatus
from critique_wheel.domain.models.iam_repository import AbstractMemberRepository
from critique_wheel.domain.services.iam_service import (
    IAMService,
    MemberNotFoundException,
    InvalidCredentials,
)


# TODO: can be moved to own file once all tests are written
class FakeMemberRepository(AbstractMemberRepository):
    def __init__(self, members: list[Member]):
        self._members = set(members)

    def add(self, member: Member) -> None:
        self._members.add(member)

    def get(self, member_id: UUID) -> Optional[Member]:
        try:
            return next(m for m in self._members if m.id == member_id)
        except StopIteration:
            raise MemberNotFoundException("Not found")

    def get_member_by_email(self, email: str) -> Optional[Member]:
        try:
            return next(m for m in self._members if m.email == email)
        except StopIteration:
            raise MemberNotFoundException("Not found")

    def list(self) -> list[Member]:
        return list(self._members)


@pytest.fixture
def member_details():
    return {
        "username": "test_username",
        "email": "test_email@davidnevin.net",
        "password": "secure_unguessable_p@ssword",
        "member_type": MemberRole.MEMBER,
        "status": MemberStatus.INACTIVE,
    }


@pytest.fixture
def repo():
    return FakeMemberRepository([])


@pytest.fixture
def service(repo):
    return IAMService(repo)


def test_create_member(repo, service, member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    member_type = member_details["member_type"]
    status = member_details["status"]

    # Act
    new_member = service.create_member(username, email, password)

    # Assert
    assert new_member is not None
    assert new_member.username == username
    assert new_member.email == email
    assert new_member.password != password
    assert new_member.member_type == member_type
    assert new_member.status == status
    assert new_member.works == []
    assert new_member.critiques == []
    assert new_member.id is not None

    assert repo.get(new_member.id) == new_member  # type: ignore
    assert repo.list() == [new_member]  # type: ignore


@pytest.mark.current
def test_member_login_valid_credentials(service, member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    new_member = service.create_member(username, email, password)

    # Act
    member = service.login_member(email, password)

    # Act
    assert member is not None
    assert member == new_member


@pytest.mark.current
def test_member_login_raises_InvalidCredentials_with_invalid_password(service, member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    service.create_member(username, email, password)
    incorrect_password = "incorrect_p2ssword"

    # Assert
    with pytest.raises(InvalidCredentials, match="Invalid credentials"):
        service.login_member(email, incorrect_password)


@pytest.mark.current
def test_member_login_raises_InvalidCredentials_for_nonexistent_email(service, member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    service.create_member(username, email, password)
    nonexistent_email = "non_exitant@davidnevin.net"

    # Assert
    with pytest.raises(InvalidCredentials, match="Invalid credentials"):
        service.login_member(nonexistent_email, password)

@pytest.mark.current
def test_new_member_with_valid_registration_creates_new_member(service, member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = member_details["password"]

    # Act
    new_member = service.register_member(username, email, password, confirm_password)

    # Assert
    assert new_member is not None
    assert new_member.username == username
    assert new_member.email == email
    assert new_member.password != password
    assert new_member.member_type == MemberRole.MEMBER
    assert new_member.status == MemberStatus.INACTIVE
    assert new_member.works == []
    assert new_member.critiques == []
    assert new_member.id is not None
