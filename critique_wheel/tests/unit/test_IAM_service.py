from uuid import uuid4

import pytest

from critique_wheel.members.exceptions import exceptions
from critique_wheel.members.models.IAM import MemberRole, MemberStatus
from critique_wheel.members.services import iam_service
from critique_wheel.members.value_objects import MemberId
from tests.integration.fake_iam_repository import FakeMemberRepository


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


def create_member_for_testing(member_details, repo, session):
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]

    return iam_service.create_member(
        username,
        email,
        password,
        repo,
        session,
    )


def test_create_member(member_details):
    # Arrange
    repo = FakeMemberRepository([])
    session = FakeSession()
    result = create_member_for_testing(member_details, repo, session)
    # Act

    # Assert
    assert result is not None
    assert isinstance(result, MemberId) is True
    assert session.committed is True


def test_login_member_valid_credentials(member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]

    repo = FakeMemberRepository([])
    session = FakeSession()
    new_member_id = iam_service.create_member(username, email, password, repo, session)

    # Act
    returned_member = iam_service.login_member(email, password, repo, session)

    # Assert
    assert returned_member is not None
    assert returned_member.id == new_member_id

    assert session.committed is True


def test_login_member_raises_InvalidCredentials_with_invalid_password(member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]

    repo = FakeMemberRepository([])
    session = FakeSession()
    iam_service.create_member(username, email, password, repo, session)

    # Assert
    with pytest.raises(iam_service.InvalidCredentials, match="Invalid credentials"):
        iam_service.login_member(email, "incorrect_password", repo, session)


def test_login_member_raises_InvalidCredentials_for_nonexistent_email(member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]

    repo = FakeMemberRepository([])
    session = FakeSession()
    iam_service.create_member(username, email, password, repo, session)
    non_existant_email = "this_email_does_not_exist@davidnevin.net"
    # Assert
    with pytest.raises(iam_service.InvalidCredentials, match="Invalid credentials"):
        iam_service.login_member(non_existant_email, password, repo, session)


def test_register_new_member_with_valid_registration_creates_new_member(member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = member_details["password"]

    repo = FakeMemberRepository([])
    session = FakeSession()
    # Act
    new_member = iam_service.register_member(
        username, email, password, confirm_password, repo, session
    )

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
    assert session.committed is True


def test_register_new_member_with_non_matching_passwords_raises_BaseIAMDomainError(
    member_details
):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    non_matching_password = "something!else@P"
    confirm_password = non_matching_password

    repo = FakeMemberRepository([])
    session = FakeSession()
    # Act

    # Assert
    with pytest.raises(exceptions.BaseIAMDomainError):
        iam_service.register_member(
            username, email, password, confirm_password, repo, session
        )


def test_register_new_member_with_missing_username_raises_BaseIAMDomainError(
    member_details
):
    # Arrange
    username = ""
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = member_details["password"]

    repo = FakeMemberRepository([])
    session = FakeSession()
    # Assert
    with pytest.raises(exceptions.BaseIAMDomainError):
        iam_service.register_member(
            username, email, password, confirm_password, repo, session
        )


def test_register_new_member_with_missing_email_raises_BaseIAMDomainError(
    member_details
):
    # Arrange
    username = member_details["username"]
    email = ""
    password = member_details["password"]
    confirm_password = member_details["password"]

    repo = FakeMemberRepository([])
    session = FakeSession()
    # Assert
    with pytest.raises(exceptions.BaseIAMDomainError):
        iam_service.register_member(
            username, email, password, confirm_password, repo, session
        )


def test_register_new_member_with_missing_password_raises_BaseIAMDomainError(
    member_details,
):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = ""
    confirm_password = member_details["password"]

    repo = FakeMemberRepository([])
    session = FakeSession()
    # Assert
    with pytest.raises(exceptions.BaseIAMDomainError):
        iam_service.register_member(
            username, email, password, confirm_password, repo, session
        )


def test_new_member_with_missing_confirm_password_raises_BaseIAMDomainError(
    member_details,
):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = ""

    repo = FakeMemberRepository([])
    session = FakeSession()
    # Assert
    with pytest.raises(exceptions.BaseIAMDomainError):
        iam_service.register_member(
            username, email, password, confirm_password, repo, session
        )


def test_new_member_with_existing_email_raises_DuplicateEntryError(
    member_details,
):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = member_details["password"]
    repo = FakeMemberRepository([])
    session = FakeSession()
    iam_service.register_member(
        username, email, password, confirm_password, repo, session
    )

    # Assert
    with pytest.raises(iam_service.DuplicateEntryError):
        iam_service.register_member(
            username, email, password, confirm_password, repo, session
        )


def test_new_member_with_existing_username_raises_DuplicateEntryError(member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = member_details["password"]
    repo = FakeMemberRepository([])
    session = FakeSession()
    iam_service.register_member(
        username, email, password, confirm_password, repo, session
    )

    # Assert
    with pytest.raises(iam_service.DuplicateEntryError):
        iam_service.register_member(
            username, email, password, confirm_password, repo, session
        )


def test_list_members(member_details):
    # Arrange
    repo = FakeMemberRepository([])
    session = FakeSession()
    new_member_1 = create_member_for_testing(member_details, repo, session)

    another_member_details = {
        "username": "other_username",
        "email": "other_email@davidnevin.net",
        "password": "other_p@ssword",
    }
    new_member_2 = create_member_for_testing(another_member_details, repo, session)

    # Act
    members_list = iam_service.list_members(repo)

    # Assert
    assert len(members_list) == 2
    assert members_list[0].id == new_member_1.id or new_member_2.id
    assert members_list[1].id == new_member_2.id or new_member_1.id


def test_list_members_returns_empty_list_when_no_members():
    # Act
    repo = FakeMemberRepository([])
    members_list = iam_service.list_members(repo)

    # Assert
    assert len(members_list) == 0


def test_get_member_by_id_returns_member_with_matching_id(member_details):
    # Arrange
    repo = FakeMemberRepository([])
    session = FakeSession()
    new_member_1 = create_member_for_testing(member_details, repo, session)

    # Act
    member = iam_service.get_member_by_id(str(new_member_1.id), repo)

    # Assert
    assert member is not None
    assert str(member.id) == str(new_member_1.id)
    assert str(member.username) == member_details["username"]


def test_get_member_by_id_returns_None_for_nonexistent_id():
    repo = FakeMemberRepository([])
    nonexistent_id = str(uuid4())
    assert iam_service.get_member_by_id(nonexistent_id, repo) is None


def test_get_member_by_username_returns_member_with_matching_username(member_details):
    # Arrange
    repo = FakeMemberRepository([])
    session = FakeSession()
    create_member_for_testing(member_details, repo, session)

    # Act
    member = iam_service.get_member_by_username(member_details["username"], repo)

    # Assert
    assert member is not None
    assert str(member.username) == member_details["username"]


def test_get_member_by_username_returns_None_for_nonexistent_username():
    repo = FakeMemberRepository([])
    nonexistent_username = "nonexistent_username"
    assert iam_service.get_member_by_username(nonexistent_username, repo) is None
