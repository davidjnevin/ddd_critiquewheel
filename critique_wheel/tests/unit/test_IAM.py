import os

import pytest

from critique_wheel.domain.models.IAM import (
    Member,
    MemberRole,
    MemberStatus,
    MissingEntryError,
)

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
        password="test_pass!",
        username="test_user",
    )


@pytest.mark.slow
@pytest.fixture
def admin():
    return Member.create(
        email="admin@example.com",
        password="admin_pass!",
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
            password="secure_unguessable_p@ssword",
            email="email_address@davidneivn.net",
            member_type=MemberRole.MEMBER,
        )
        assert member.username == "test_username"
        assert member.password != "secure_unguessable_p@ssword"
        assert member.email == "email_address@davidneivn.net"
        assert member.member_type == MemberRole.MEMBER
        assert member.works == []
        assert member.critiques == []

    def test_create_with_missing_username(self):
        with pytest.raises(
            MissingEntryError,
            match="Missing required fields",
        ):
            Member.create(
                username="",  # "username" is intentionally omitted
                password="secure_unguessable_p@ssword",
                email="email_address@davidnevin.net",
            )

    def test_member_registration(self):
        member = Member.register(**registration_details)
        assert member.email == registration_details["email"]
        assert member.username == registration_details["username"]
        # Ensure the password is hashed and not stored in plain text
        assert member.password != registration_details["password"]

    def test_member_registration_missing_username(self):
        with pytest.raises(
            MissingEntryError,
            match="Missing required fields: username",
        ):
            registration_details = {
                "username": "",  # "username" is intentionally omitted
                "email": "test@example.com",
                "password": "test_pass!",
            }
            Member.register(**registration_details)

    def test_member_registration_missing_email(self):
        with pytest.raises(
            MissingEntryError,
            match="Missing required fields: email",
        ):
            registration_details = {
                "username": "test_user",
                "email": "",  # "email" is intentionally omitted
                "password": "test_pass",
            }
            Member.register(**registration_details)

    def test_member_registration_missing_password(self):
        with pytest.raises(
            MissingEntryError,
            match="Missing required fields: password",
        ):
            registration_details = {
                "username": "test_user",
                "email": "test@example.com",
                "password": "",  # "password" is intentionally omitted
            }
            Member.register(**registration_details)


    def test_password_change_correct_old_password(self, member):
        member.change_password(old_password="test_pass!", new_password="new_p@ssword")
        assert member.verify_password("new_p@ssword")

    def test_password_change_incorrect_old_password(self, member):
        with pytest.raises(ValueError, match="Incorrect old password"):
            member.change_password(old_password="wrong_old_p@ssword", new_password="new_p@ssword")

    def test_validate_password_strength(self):
        Member.validate_password_strength("secure_p@ssword")
        with pytest.raises(
            ValueError,
            match="Password does not meet the policy requirements: Minimum length of 8 characters required",
        ):
            Member.validate_password_strength("short")
        with pytest.raises(
            ValueError,
            match="Password does not meet the policy requirements: Mix of letters, numbers, and symbols required.",
        ):
            Member.validate_password_strength("allletters")
        with pytest.raises(
            ValueError,
            match="Password does not meet the policy requirements: Mix of letters, numbers, and symbols required.",
        ):
            Member.validate_password_strength("123499900990990")
        with pytest.raises(
            ValueError,
            match="Password does not meet the policy requirements: Mix of letters, numbers, and symbols required.",
        ):
            Member.validate_password_strength("123helloworld")
        with pytest.raises(
            ValueError,
            match="Password does not meet the policy requirements: Password is easily guessable.",
        ):
            Member.validate_password_strength("password10!")


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
            PermissionError,
            match="Only admins can deactivate members.",
        ):
            another_member.deactivate_member(member)
        assert member.status == MemberStatus.INACTIVE

    def test_email_verification_code_generation(self, member):
        verification_code = member.generate_email_verification_code()
        assert verification_code is not None
        # TODO: Check if the code was sent via Notification Context


@pytest.mark.slow
class TestPassWordStrength:
    def setup_method(self):
        mock_db.clear()

    def test_password_policy_enforcement(self):
        weak_passwords = ["password", "abcdefg", "12345678", "qwerty"]
        for password in weak_passwords:
            with pytest.raises(ValueError, match="Password does not meet the policy requirements"):
                Member.register(username="test_user", email="test@example.com", password=password)

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
            (MemberRole.STAFF, "delete", "Works", False),  # Staff shouldn't have delete permission on Works
            (MemberRole.MEMBER, "read", "Works", True),
            (MemberRole.MEMBER, "write", "Critiques", True),
            (MemberRole.MEMBER, "delete", "Works", False),  # Member shouldn't have delete permission on Works
        ],
    )
    def test_has_permission(self, mock_roles, member_type, action, resource, expected):
        member = Member(member_type=member_type, username="test_user", email="test@example.com", password="test_pass!")
        assert member.has_permission(action, resource) == expected


class TestMemberContributions:
    def setup_method(self):
        mock_db.clear()

    def test_member_works(self, member, valid_work):
        assert member.works == []
        member.works.append(valid_work)
        assert member.list_works() == [valid_work]

    def test_add_work_to_member(self, member, valid_work):
        assert member.works == []
        member.add_work(valid_work)
        assert member.works == [valid_work]

        with pytest.raises(
            ValueError,
            match="Work already exists",
        ):
            member.add_work(valid_work)

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

    def test_add_critique_to_member(self, valid_member, valid_critique):
        reviewer = valid_member
        reviewer.status = MemberStatus.ACTIVE
        assert reviewer.critiques == []
        valid_critique.member_id = reviewer.id
        reviewer.add_critique(valid_critique)
        assert reviewer.critiques == [valid_critique]

        with pytest.raises(
            ValueError,
            match="Critique already exists",
        ):
            reviewer.add_critique(valid_critique)
