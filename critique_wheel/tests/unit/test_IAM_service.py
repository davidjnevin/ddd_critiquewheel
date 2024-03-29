import uuid
from uuid import uuid4

import pytest

from critique_wheel.members.models.IAM import MemberRole, MemberStatus
from critique_wheel.members.services import exceptions as service_exceptions
from critique_wheel.members.services import iam_service, unit_of_work
from critique_wheel.members.value_objects import MemberId
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


def test_add_member_raises_InvalidCredentialsError_with_invalid_password(
    member_details,
):
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
    with pytest.raises(
        service_exceptions.InvalidCredentialsError, match="Invalid credentials"
    ):
        iam_service.login_member(
            uow,
            email,
            "incorrect_password",
        )


def test_login_member_raises_InvalidCredentialsError_for_nonexistent_email(
    member_details,
):
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
    with pytest.raises(
        service_exceptions.InvalidCredentialsError, match="Invalid credentials"
    ):
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


def test_register_new_member_with_non_matching_passwords_raises_PasswordMismatchError(
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
    with pytest.raises(
        service_exceptions.PasswordMismatchError,
        match="Password and confirm password do not match",
    ):
        iam_service.register_member(
            uow,
            username,
            email,
            password,
            confirm_password,
        )


def test_register_new_member_with_missing_username_raises_MissingUsernameError(
    member_details,
):
    # Arrange
    username = ""
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = member_details["password"]
    uow = FakeUnitOfWork()

    # Assert
    with pytest.raises(service_exceptions.MissingUsernameError):
        iam_service.register_member(
            uow,
            username,
            email,
            password,
            confirm_password,
        )


def test_register_new_member_with_missing_email_raises_MissingEmailError(
    member_details,
):
    # Arrange
    username = member_details["username"]
    email = ""
    password = member_details["password"]
    confirm_password = member_details["password"]
    uow = FakeUnitOfWork()

    # Assert
    with pytest.raises(service_exceptions.MissingEmailError):
        iam_service.register_member(
            uow,
            username,
            email,
            password,
            confirm_password,
        )


def test_register_new_member_with_missing_password_raises_MissingPasswordError(
    member_details,
):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = ""
    confirm_password = member_details["password"]
    uow = FakeUnitOfWork()

    # Assert
    with pytest.raises(service_exceptions.MissingPasswordError):
        iam_service.register_member(
            uow,
            username,
            email,
            password,
            confirm_password,
        )


def test_register_new_member_with_missing_confirm_password_raises_MissingConfirmPasswordError(
    member_details,
):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    password = member_details["password"]
    confirm_password = ""
    uow = FakeUnitOfWork()

    # Assert
    with pytest.raises(service_exceptions.PasswordMismatchError):
        iam_service.register_member(
            uow,
            username,
            email,
            password,
            confirm_password,
        )


def test_register_new_member_with_existing_email_raises_DuplicateEntryError(
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
    with pytest.raises(service_exceptions.DuplicateEntryError):
        iam_service.register_member(
            uow,
            username,
            email,
            password,
            confirm_password,
        )


def test_register_new_member_with_existing_username_raises_DuplicateUsernameError(
    member_details,
):
    # Arrange
    username = member_details["username"]
    email = member_details["email"]
    email_2 = "random_text" + email
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
    with pytest.raises(service_exceptions.DuplicateUsernameError):
        iam_service.register_member(
            uow,
            username,
            email_2,
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
    new_member_dict = iam_service.add_member(
        uow,
        username,
        email,
        password,
    )
    # convert new_member_dict["id"] to a MemberId object
    member_id = MemberId(uuid.UUID(new_member_dict["id"]))
    # Act
    member = iam_service.get_member_by_id(member_id, uow)

    # Assert
    assert member is not None
    assert str(member.id) == str(new_member_dict["id"])
    assert str(member.username) == member_details["username"]


def test_get_member_by_id_for_nonexistent_id_raises_MemberNotFoundError():
    uow = FakeUnitOfWork()
    nonexistent_id = MemberId(uuid4())
    with pytest.raises(service_exceptions.MemberNotFoundError):
        iam_service.get_member_by_id(nonexistent_id, uow)


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


def test_get_member_by_username_raises_MemberNotFoundError_for_nonexistent_username():
    uow = FakeUnitOfWork()
    nonexistent_username = "nonexistent_username"
    with pytest.raises(service_exceptions.MemberNotFoundError):
        iam_service.get_member_by_username(nonexistent_username, uow)
