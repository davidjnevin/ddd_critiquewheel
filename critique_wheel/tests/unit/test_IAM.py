import os

import pytest

from critique_wheel.members.models import exceptions
from critique_wheel.members.models.IAM import Member, MemberRole, MemberStatus

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MOCK_YAML_PATH = os.path.join(CURRENT_DIR, "mock_rbac.yaml")

mock_db = {}

registration_details = {
    "email": "test@example.com",
    "password": "secure_p@ssword",
    "username": "test_user",
}


@pytest.fixture
def member():
    return Member.create(
        email="test@example.com",
        password="test_pass10!",
        username="test_user",
    )


@pytest.mark.slow
@pytest.fixture
def admin():
    return Member.create(
        email="admin@example.com",
        password="admin_pass10!",
        username="admin_user",
        member_type=MemberRole.ADMIN,
    )


@pytest.mark.slow
class TestRegistrationAndLogin:
    def setup_method(self):
        mock_db.clear()

    def test_member_create(self):
        member = Member.create(
            username="test_username",
            password="secure_unguessab1e_p@ssword",
            email="email_address@davidneivn.net",
            member_type=MemberRole.MEMBER,
        )
        assert member.username == "test_username"
        assert member.password != "secure_unguessab1e_p@ssword"
        assert member.email == "email_address@davidneivn.net"
        assert member.member_type == MemberRole.MEMBER
        assert member.works == []
        assert member.critiques == []

    def test_create_with_missing_username(self):
        with pytest.raises(
            exceptions.MissingEntryError,
            match="Missing required fields",
        ):
            Member.create(
                username="",  # "username" is intentionally omitted
                password="secure_unguessable_p@ssword",
                email="email_address@davidnevin.net",
            )

    def test_password_change_correct_old_password(self, member):
        member.change_password(
            old_password="test_pass10!", new_password="new_p@ssword10"
        )
        assert member.verify_password("new_p@ssword10")

    def test_password_change_incorrect_old_password(self, member):
        with pytest.raises(
            exceptions.IncorrectCredentialsError, match="Incorrect old password"
        ):
            member.change_password(
                old_password="wrong_old_p@ssword", new_password="new_p@ssword"
            )

    def test_validate_password_strength(self):
        assert Member.validate_password_strength("secure_p@ssword!10") is None

    def test_validate_password_strength_too_short(self):
        with pytest.raises(
            exceptions.WeakPasswordError,
            match="Password does not meet the policy requirements: Minimum length of 8 characters required",
        ):
            Member.validate_password_strength("short")

    def test_validate_password_strength_all_letters(self):
        with pytest.raises(
            exceptions.WeakPasswordError,
            match="Password does not meet the policy requirements: Mix of letters, numbers, and symbols required.",
        ):
            Member.validate_password_strength("allletters")

    def test_validate_password_strength_all_numbers(self):
        with pytest.raises(
            exceptions.WeakPasswordError,
            match="Password does not meet the policy requirements: Mix of letters, numbers, and symbols required.",
        ):
            Member.validate_password_strength("123499900990990")

    def test_validate_password_strength_no_symbols(self):
        with pytest.raises(
            exceptions.WeakPasswordError,
            match="Password does not meet the policy requirements: Mix of letters, numbers, and symbols required.",
        ):
            Member.validate_password_strength("123helloworld")

    def test_validate_password_strength_easily_guessable(self):
        weak_passwords = ["password", "abcdefg", "12345678", "qwerty"]
        for password in weak_passwords:
            with pytest.raises(exceptions.WeakPasswordError):
                Member.create(
                    username="test_user", email="test@example.com", password=password
                )


class TestMemberActivationEmailVerification:
    def setup_method(self):
        mock_db.clear()

    def test_member_self_deactivation(self, member):
        member.deactivate_self()
        assert member.status == MemberStatus.INACTIVE

    def test_admin_member_deactivation(self, admin, member):
        admin.deactivate_member(member)
        assert member.status == MemberStatus.INACTIVE

    def test_non_admin_member_deactivation(self, admin, member):
        admin.member_type = MemberRole.MEMBER
        another_member = admin
        with pytest.raises(
            exceptions.AdminOnlyError,
            match="Only admins can deactivate members.",
        ):
            another_member.deactivate_member(member)
        assert member.status == MemberStatus.INACTIVE

    def test_email_verification_code_generation(self, member):
        verification_code = member.generate_email_verification_code()
        assert verification_code is not None
        # TODO: Check if the code was sent via Notification Context


@pytest.mark.slow
class TestPassReset:
    def setup_method(self):
        mock_db.clear()

    def test_password_reset_request(self, member):
        reset_token = member.request_password_reset()
        assert reset_token is not None

    def test_password_reset_with_valid_token(self, member):
        reset_token = member.request_password_reset()
        new_password = "new_test_pass!"
        member.reset_password(token=reset_token, new_password=new_password)
        assert member.verify_password(new_password)

    def test_password_reset_with_invalid_token(self, member):
        invalid_token = "invalid_token"
        with pytest.raises(ValueError, match="Invalid reset token"):
            member.reset_password(token=invalid_token, new_password="new_test_pass")


@pytest.fixture(scope="class")
def mock_roles():
    assert os.path.exists(MOCK_YAML_PATH), f"File not found at {MOCK_YAML_PATH}"
    # Load roles and permissions from the mock YAML file
    Member.load_roles_from_yaml(file_path=MOCK_YAML_PATH)


class TestRoles:
    def test_load_roles_from_yaml(self, mock_roles):
        assert Member.ROLES_AND_PERMISSIONS is not None
        assert "ADMIN" in Member.ROLES_AND_PERMISSIONS
        assert "STAFF" in Member.ROLES_AND_PERMISSIONS
        assert "MEMBER" in Member.ROLES_AND_PERMISSIONS

    @pytest.mark.parametrize(
        "member_type, action, resource, expected",
        [
            (MemberRole.ADMIN, "read", "Works", True),
            (MemberRole.ADMIN, "write", "Works", True),
            (MemberRole.ADMIN, "delete", "Works", True),
            (MemberRole.ADMIN, "read", "Critiques", True),
            (MemberRole.ADMIN, "write", "Critiques", True),
            (MemberRole.ADMIN, "read", "Profiles", True),
            (MemberRole.ADMIN, "write", "Profiles", True),
            (MemberRole.ADMIN, "read", "Members", True),
            (MemberRole.ADMIN, "write", "Members", True),
            (MemberRole.STAFF, "read", "Works", True),
            (MemberRole.STAFF, "write", "Critiques", True),
            (
                MemberRole.STAFF,
                "delete",
                "Works",
                False,
            ),  # Staff shouldn't have delete permission on Works
            (MemberRole.MEMBER, "read", "Works", True),
            (MemberRole.MEMBER, "write", "Critiques", True),
            (
                MemberRole.MEMBER,
                "delete",
                "Works",
                False,
            ),  # Member shouldn't have delete permission on Works
        ],
    )
    def test_has_permission(self, mock_roles, member_type, action, resource, expected):
        member = Member(
            member_type=member_type,
            username="test_user",
            email="test@example.com",
            password="test_pass!",
        )
        assert member.has_permission(action, resource) == expected


class TestMemberContributions:
    def setup_method(self):
        mock_db.clear()

    def test_member_works(self, member, valid_work):
        assert member.works == []
        member.works.append(valid_work)
        assert member.list_works() == [valid_work]

    def test_member_critiques(self, valid_member, member, valid_work, valid_critique):
        assert member.critiques == []
        assert valid_member.critiques == []

        writer = member
        reviewer = valid_member

        valid_work.member_id = writer.id
        writer.works.append(valid_work)
        valid_critique.member_id = reviewer.id
        valid_work.critiques.append(valid_critique)
        reviewer.critiques.append(valid_critique)
        assert reviewer.list_critiques() == [valid_critique]
