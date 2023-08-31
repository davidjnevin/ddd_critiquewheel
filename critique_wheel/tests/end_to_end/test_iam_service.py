from typing import Optional

import pytest
from sqlalchemy import UUID

from critique_wheel.domain.models.IAM import Member, MemberRole, MemberStatus
from critique_wheel.domain.models.iam_repository import AbstractMemberRepository
from critique_wheel.domain.services.iam_service import (
    IAMService,
    MemberNotFoundException,
    InvalidCredentials,
    NonMatchingPasswords,
    MissingEntryError,
    DuplicateEmailError,
    DuplicateUsernameError
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

    def get_member_by_username(self, username: str) -> Optional[Member]:
        try:
            return next(m for m in self._members if m.username == username)
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


def test_login_member_valid_credentials(service, member_details):
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


def test_login_member_raises_InvalidCredentials_with_invalid_password(service, member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    service.create_member(username, email, password)
    incorrect_password = "incorrect_p2ssword"

    # Assert
    with pytest.raises(InvalidCredentials, match="Invalid credentials"):
        service.login_member(email, incorrect_password)


def test_login_member_raises_InvalidCredentials_for_nonexistent_email(service, member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    service.create_member(username, email, password)
    nonexistent_email = "non_exitant@davidnevin.net"

    # Assert
    with pytest.raises(InvalidCredentials, match="Invalid credentials"):
        service.login_member(nonexistent_email, password)

def test_register_new_member_with_valid_registration_creates_new_member(service, member_details):
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

def test_register_new_member_with_non_matching_passwords_raises_NonMatchingPasswords(service, member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = "non_matching_p@ssword"

    # Assert
    with pytest.raises(NonMatchingPasswords):
        new_member = service.register_member(username, email, password, confirm_password)

def test_register_new_member_with_missing_username_raises_MissingEntryError(service, member_details):
    # Arrange
    username = ""
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = member_details["password"]

    # Assert
    with pytest.raises(MissingEntryError):
        new_member = service.register_member(username, email, password, confirm_password)

def test_register_new_member_with_missing_email_raises_MissingEntryError(service, member_details):
    # Arrange
    username = member_details["username"]
    email = ""
    password = member_details["password"]
    confirm_password = member_details["password"]

    # Assert
    with pytest.raises(MissingEntryError):
        new_member = service.register_member(username, email, password, confirm_password)

def test_register_new_member_with_missing_password_raises_MissingEntryError(service, member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = ""
    confirm_password = member_details["password"]

    # Assert
    with pytest.raises(MissingEntryError):
        new_member = service.register_member(username, email, password, confirm_password)

def test_new_member_with_missing_confirm_password_raises_MissingEntryError(service, member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = ""

    # Assert
    with pytest.raises(MissingEntryError):
        new_member = service.register_member(username, email, password, confirm_password)

def test_new_member_with_existing_email_raises_DuplicateEmailError(service, member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = member_details["password"]
    service.register_member(username, email, password, confirm_password)

    # Assert
    with pytest.raises(DuplicateEmailError):
        new_member = service.register_member(username, email, password, confirm_password)


def test_new_member_with_existing_username_raises_DuplicateUsernameError(service, member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = member_details["password"]
    service.register_member(username, email, password, confirm_password)
    other_email = "other_email@davidnevin.net"

    # Assert
    with pytest.raises(DuplicateUsernameError):
        new_member = service.register_member(username, other_email, password, confirm_password)
