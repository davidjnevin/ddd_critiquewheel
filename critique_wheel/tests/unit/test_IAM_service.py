import pytest

from critique_wheel.members.models.IAM import MemberRole, MemberStatus
from critique_wheel.members.models.IAM_domain_exceptions import BaseIAMDomainError
from critique_wheel.members.services.iam_service import (
    DuplicateEntryError,
    InvalidCredentials,
)


def test_create_member(iam_repo, iam_service, member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    member_type = member_details["member_type"]
    status = member_details["status"]

    # Act
    new_member = iam_service.create_member(username, email, password)

    # Assert
    assert new_member is not None
    assert new_member.username == username
    assert new_member.email == email
    assert new_member.password != password
    assert new_member.member_type == member_type
    assert new_member.status == status
    assert new_member.works == []
    assert new_member.critiques == []

    assert iam_repo.get_member_by_id(new_member.id) == new_member  # type: ignore
    assert iam_repo.list() == [new_member]  # type: ignore


def test_login_member_valid_credentials(iam_service, member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    new_member = iam_service.create_member(username, email, password)

    # Act
    member = iam_service.login_member(email, password)

    # Act
    assert member is not None
    assert member == new_member


def test_login_member_raises_InvalidCredentials_with_invalid_password(
    iam_service, member_details
):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    iam_service.create_member(username, email, password)
    incorrect_password = "incorrect_p2ssword"

    # Assert
    with pytest.raises(InvalidCredentials, match="Invalid credentials"):
        iam_service.login_member(email, incorrect_password)


def test_login_member_raises_InvalidCredentials_for_nonexistent_email(
    iam_service, member_details
):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    iam_service.create_member(username, email, password)
    nonexistent_email = "non_exitant@davidnevin.net"

    # Assert
    with pytest.raises(InvalidCredentials, match="Invalid credentials"):
        iam_service.login_member(nonexistent_email, password)


def test_register_new_member_with_valid_registration_creates_new_member(
    iam_service, member_details
):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = member_details["password"]

    # Act
    new_member = iam_service.register_member(
        username, email, password, confirm_password
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


def test_register_new_member_with_non_matching_passwords_raises_BaseIAMDomainError(
    iam_service, member_details
):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = "non_matching_p@ssword"

    # Assert
    with pytest.raises(BaseIAMDomainError):
        iam_service.register_member(username, email, password, confirm_password)


def test_register_new_member_with_missing_username_raises_BaseIAMDomainError(
    iam_service, member_details
):
    # Arrange
    username = ""
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = member_details["password"]

    # Assert
    with pytest.raises(BaseIAMDomainError):
        iam_service.register_member(username, email, password, confirm_password)


def test_register_new_member_with_missing_email_raises_BaseIAMDomainError(
    iam_service, member_details
):
    # Arrange
    username = member_details["username"]
    email = ""
    password = member_details["password"]
    confirm_password = member_details["password"]

    # Assert
    with pytest.raises(BaseIAMDomainError):
        iam_service.register_member(username, email, password, confirm_password)


def test_register_new_member_with_missing_password_raises_BaseIAMDomainError(
    iam_service, member_details
):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = ""
    confirm_password = member_details["password"]

    # Assert
    with pytest.raises(BaseIAMDomainError):
        iam_service.register_member(username, email, password, confirm_password)


def test_new_member_with_missing_confirm_password_raises_BaseIAMDomainError(
    iam_service, member_details
):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = ""

    # Assert
    with pytest.raises(BaseIAMDomainError):
        iam_service.register_member(username, email, password, confirm_password)


def test_new_member_with_existing_email_raises_DuplicateEntryError(
    iam_service, member_details
):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = member_details["password"]
    iam_service.register_member(username, email, password, confirm_password)

    # Assert
    with pytest.raises(DuplicateEntryError):
        iam_service.register_member(username, email, password, confirm_password)


def test_new_member_with_existing_username_raises_DuplicateEntryError(
    iam_service, member_details
):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = member_details["password"]
    iam_service.register_member(username, email, password, confirm_password)
    other_email = "other_email@davidnevin.net"

    # Assert
    with pytest.raises(DuplicateEntryError):
        iam_service.register_member(username, other_email, password, confirm_password)


def test_list_members(iam_service, member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    new_member = iam_service.create_member(username, email, password)

    username = "other_username"
    email = "other_email@davidnevin.net"
    password = "other_p@ssword"
    new_member_2 = iam_service.create_member(username, email, password)

    # Act
    members_list = iam_service.list_members()

    # Assert
    assert len(members_list) == 2
    assert new_member and new_member_2 in members_list


def test_list_members_returns_empty_list_when_no_members(iam_service):
    # Act
    members_list = iam_service.list_members()

    # Assert
    assert len(members_list) == 0


def test_get_member_by_id_returns_member_with_matching_id(iam_service, member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    new_member = iam_service.create_member(username, email, password)

    # Act
    member = iam_service.get_member_by_id(new_member.id)

    # Assert
    assert member is not None
    assert member == new_member


def test_get_member_by_id_returns_None_for_nonexistent_id(iam_service, member_details):
    nonexistent_id = 999
    assert iam_service.get_member_by_id(nonexistent_id) is None


def test_get_member_by_username_returns_member_with_matching_username(
    iam_service, member_details
):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    new_member = iam_service.create_member(username, email, password)

    # Act
    member = iam_service.get_member_by_username(username)

    # Assert
    assert member is not None
    assert member == new_member


def test_get_member_by_username_returns_None_for_nonexistent_username(iam_service):
    nonexistent_username = "nonexistent_username"
    assert iam_service.get_member_by_username(nonexistent_username) is None


def test_add_work_to_member_adds_work_to_member(
    iam_service, member_details, work_service, work_details
):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    new_member = iam_service.create_member(username, email, password)

    title = work_details["title"]
    content = work_details["content"]
    genre = work_details["genre"]
    age_restriction = work_details["age_restriction"]

    new_work = work_service.add_work(
        title=title,
        content=content,
        genre=genre,
        age_restriction=age_restriction,
        member_id=new_member.id,
    )

    # Act
    iam_service.add_work_to_member(member_id=new_member.id, work=new_work)

    # Assert
    assert len(new_member.works) == 1
    assert new_work in new_member.works
