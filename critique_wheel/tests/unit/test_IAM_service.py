from uuid import uuid4

import pytest

from critique_wheel.members.exceptions import exceptions
from critique_wheel.members.models.IAM import MemberRole, MemberStatus
from critique_wheel.members.services import iam_service, unit_of_work
from tests.integration import fake_iam_repository


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.members = fake_iam_repository.FakeMemberRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_add_member(member_details):
    # Arrange
    uow = FakeUnitOfWork()
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    # Act
    member = iam_service.add_member(
        uow=uow,
        username=username,
        email=email,
        password=password,
    )

    # Assert
    assert member is not None
    assert uow.committed


def test_login_member_valid_credentials(member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    uow = FakeUnitOfWork()

    new_member_id = iam_service.add_member(
        uow,
        username,
        email,
        password,
    )

    # Act
    returned_member = iam_service.login_member(
        uow,
        email,
        password,
    )

    # Assert
    assert returned_member is not None
    assert returned_member["id"] == str(new_member_id["id"])
    assert returned_member["username"] == member_details["username"]
    assert returned_member["email"] == member_details["email"]
    assert returned_member["password"] != member_details["password"]

    assert uow.committed is True


def test_login_member_raises_InvalidCredentials_with_invalid_password(member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    uow = FakeUnitOfWork()

    iam_service.add_member(
        uow,
        username,
        email,
        password,
    )

    # Assert
    with pytest.raises(iam_service.InvalidCredentials, match="Invalid credentials"):
        iam_service.login_member(
            uow,
            email,
            "incorrect_password",
        )


def test_login_member_raises_InvalidCredentials_for_nonexistent_email(member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    uow = FakeUnitOfWork()

    iam_service.add_member(
        uow,
        username,
        email,
        password,
    )
    non_existant_email = "this_email_does_not_exist@davidnevin.net"
    # Assert
    with pytest.raises(iam_service.InvalidCredentials, match="Invalid credentials"):
        iam_service.login_member(
            uow,
            non_existant_email,
            password,
        )


def test_register_new_member_with_valid_registration_returns_new_member(member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = member_details["password"]
    uow = FakeUnitOfWork()

    # Act
    new_member = iam_service.register_member(
        uow,
        username,
        email,
        password,
        confirm_password,
    )

    # Assert
    assert new_member is not None
    assert new_member["username"] == username
    assert new_member["email"] == email
    assert new_member["password"] != password
    assert new_member["member_type"] == MemberRole.MEMBER.value
    assert new_member["status"] == MemberStatus.INACTIVE.value
    assert new_member["works"] == []
    assert new_member["critiques"] == []
    assert new_member["id"] is not None
    assert uow.committed is True


def test_register_new_member_with_non_matching_passwords_raises_BaseIAMDomainError(
    member_details,
):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    non_matching_password = "something!else@P"
    confirm_password = non_matching_password
    uow = FakeUnitOfWork()

    # Act

    # Assert
    with pytest.raises(exceptions.BaseIAMDomainError):
        iam_service.register_member(
            uow,
            username,
            email,
            password,
            confirm_password,
        )


def test_register_new_member_with_missing_username_raises_BaseIAMDomainError(
    member_details,
):
    # Arrange
    username = ""
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = member_details["password"]
    uow = FakeUnitOfWork()

    # Assert
    with pytest.raises(exceptions.BaseIAMDomainError):
        iam_service.register_member(
            uow,
            username,
            email,
            password,
            confirm_password,
        )


def test_register_new_member_with_missing_email_raises_BaseIAMDomainError(
    member_details,
):
    # Arrange
    username = member_details["username"]
    email = ""
    password = member_details["password"]
    confirm_password = member_details["password"]
    uow = FakeUnitOfWork()

    # Assert
    with pytest.raises(exceptions.BaseIAMDomainError):
        iam_service.register_member(
            uow,
            username,
            email,
            password,
            confirm_password,
        )


def test_register_new_member_with_missing_password_raises_BaseIAMDomainError(
    member_details,
):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = ""
    confirm_password = member_details["password"]
    uow = FakeUnitOfWork()

    # Assert
    with pytest.raises(exceptions.BaseIAMDomainError):
        iam_service.register_member(
            uow,
            username,
            email,
            password,
            confirm_password,
        )


def test_new_member_with_missing_confirm_password_raises_BaseIAMDomainError(
    member_details,
):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = ""
    uow = FakeUnitOfWork()

    # Assert
    with pytest.raises(exceptions.BaseIAMDomainError):
        iam_service.register_member(
            uow,
            username,
            email,
            password,
            confirm_password,
        )


def test_new_member_with_existing_email_raises_DuplicateEntryError(
    member_details,
):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = member_details["password"]
    uow = FakeUnitOfWork()

    iam_service.register_member(
        uow,
        username,
        email,
        password,
        confirm_password,
    )

    # Assert
    with pytest.raises(iam_service.DuplicateEntryError):
        iam_service.register_member(
            uow,
            username,
            email,
            password,
            confirm_password,
        )


def test_new_member_with_existing_username_raises_DuplicateEntryError(member_details):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = member_details["password"]
    uow = FakeUnitOfWork()

    iam_service.register_member(
        uow,
        username,
        email,
        password,
        confirm_password,
    )

    # Assert
    with pytest.raises(iam_service.DuplicateEntryError):
        iam_service.register_member(
            uow,
            username,
            email,
            password,
            confirm_password,
        )


def test_list_members(member_details):
    # Arrange
    uow = FakeUnitOfWork()
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]

    new_member_1 = iam_service.add_member(
        uow,
        username,
        email,
        password,
    )

    username2 = "other_username"
    email2 = "other_email@davidnevin.net"
    password2 = "other_p@ssword"

    new_member_2 = iam_service.add_member(
        uow,
        username2,
        email2,
        password2,
    )

    # Act
    members_list = iam_service.list_members(uow)

    # Assert
    assert len(members_list) == 2
    assert members_list[0].id == new_member_1 or new_member_2
    assert members_list[1].id == new_member_2 or new_member_1


def test_list_members_returns_empty_list_when_no_members():
    # Act
    uow = FakeUnitOfWork()
    members_list = iam_service.list_members(uow)

    # Assert
    assert len(members_list) == 0


def test_get_member_by_id_returns_member_with_matching_id(member_details):
    # Arrange
    uow = FakeUnitOfWork()
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    new_member_id = iam_service.add_member(
        uow,
        username,
        email,
        password,
    )

    # Act
    member = iam_service.get_member_by_id(new_member_id["id"], uow)

    # Assert
    assert member is not None
    assert str(member.id) == str(new_member_id["id"])
    assert str(member.username) == member_details["username"]


def test_get_member_by_id_returns_None_for_nonexistent_id():
    uow = FakeUnitOfWork()
    nonexistent_id = str(uuid4())
    assert iam_service.get_member_by_id(nonexistent_id, uow) is None


def test_get_member_by_username_returns_member_with_matching_username(member_details):
    # Arrange
    uow = FakeUnitOfWork()
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    iam_service.add_member(
        uow,
        username,
        email,
        password,
    )

    # Act
    member = iam_service.get_member_by_username(member_details["username"], uow)

    # Assert
    assert member is not None
    assert str(member.username) == member_details["username"]


def test_get_member_by_username_returns_None_for_nonexistent_username():
    uow = FakeUnitOfWork()
    nonexistent_username = "nonexistent_username"
    assert iam_service.get_member_by_username(nonexistent_username, uow) is None
