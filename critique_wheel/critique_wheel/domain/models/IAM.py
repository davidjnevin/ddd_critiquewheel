import os
import random
import string
from datetime import datetime
from enum import Enum
from uuid import uuid4

import bcrypt
import yaml
from dotenv import load_dotenv

load_dotenv()

ROLES_FILE_PATH = os.getenv("ROLES_FILE_PATH")

assert os.path.exists(ROLES_FILE_PATH), f"File not found at {MOCK_YAML_PATH}"
# Mock database to facilitate testing and building domain logic without a database
mock_db = {}
bcrypt.gensalt(rounds=4)  # Set the number of rounds for testing to 4


class MissingEntryError(Exception):
    pass


class MemberStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    SUSPENDED = "Suspended"
    MARKER_FOR_DELETION = "Deleted"


class MemberRole(str, Enum):
    ADMIN = "Admin"
    STAFF = "Staff"
    MEMBER = "Member"


class Permission:
    def __init__(self, action, resource):
        self.action = action
        self.resource = resource


class Member:
    # low number of roles, the in-memory approach is efficient and offers fast permission checks.
    # The potential drawbacks are manageable and can be addressed as the application grows or requirements change.
    # This avoid the need to query the yaml file for every request.
    ROLES_AND_PERMISSIONS = {}

    def __init__(
        self,
        username,
        email,
        password,
        member_type=MemberRole.MEMBER,
        status=MemberStatus.INACTIVE,
        member_id=None,
    ):
        self.id = member_id or uuid4()
        self.username: str = username
        self.email: str = email
        self.password: bytes = password
        self.member_type: MemberRole = member_type
        self.status: MemberStatus = status
        self.last_login: datetime = datetime.now()
        self.last_updated_date: datetime = datetime.now()
        self.created_date: datetime = datetime.now()

    @staticmethod
    def hash_password(password: str) -> bytes:
        bcrypt.gensalt(rounds=4)  # Set the number of rounds for testing to 4
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)

    @classmethod
    def create(
        cls,
        username,
        email,
        password,
        member_type=MemberRole.MEMBER,
    ):
        if not username:
            raise MissingEntryError("Missing required fields: username")
        if not email:
            raise MissingEntryError("Missing required fields: email")
        if not password:
            raise MissingEntryError("Missing required fields: password")
        hashed_password = cls.hash_password(password)
        return cls(
            username=username,
            email=email,
            password=hashed_password,
            member_type=member_type,
        )

    @classmethod
    def register(cls, username, email, password):
        if not username or not email or not password:
            raise MissingEntryError("Missing required fields")
        cls.validate_password_strength(password)
        hashed_password = cls.hash_password(password)
        member = cls(username=username, email=email, password=hashed_password)
        mock_db[email] = member
        return member

    @classmethod
    def login(cls, email, password):
        member = mock_db.get(email)
        if member and bcrypt.checkpw(password.encode(), member.password):
            return member
        raise ValueError("Invalid credentials")

    def change_password(self, old_password, new_password):
        self.validate_password_strength(new_password)
        if not bcrypt.checkpw(old_password.encode(), self.password):
            raise ValueError("Incorrect old password")
        self.password = self.hash_password(new_password)

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password)

    def deactivate_self(self):
        self.status = MemberStatus.INACTIVE

    def deactivate_member(self, member):
        if self.member_type != MemberRole.ADMIN:
            raise PermissionError("Only admins can deactivate members.")
        member.status = MemberStatus.INACTIVE

    def generate_email_verification_code(self):
        # TODO: Implement email verification code generation
        return "".join(random.choices(string.ascii_letters + string.digits, k=6))

    @staticmethod
    def validate_password_strength(password: str):
        if len(password) < 8:
            raise ValueError("Password does not meet the policy requirements: Minimum length of 8 characters required.")
        if password.isalpha() or password.isdigit() or password.isalnum():
            raise ValueError(
                "Password does not meet the policy requirements: Mix of letters, numbers, and symbols required."
            )
        if password.lower() in ["password", "abcdefg", "12345678", "qwerty"]:
            raise ValueError("Password does not meet the policy requirements: Password is easily guessable.")

    def request_password_reset(self):
        # TODO: Implement token generation logic
        # For simplicity, we'll use a random string as the token.
        # In a real-world scenario, you'd want a more secure token generation mechanism.
        token = "".join(random.choices(string.ascii_letters + string.digits, k=32))
        # TODO: Store the token in the database with an expiration time
        # TODO: Send the token via the Notification Context
        return token

    def reset_password(self, token, new_password):
        # TODO: Validate the token against the database and check its expiration
        # For this example, assume the token is always valid.
        # In a real-world scenario, validate the token against stored tokens in the database.
        if token == "invalid_token":
            raise ValueError("Invalid reset token")
        self.validate_password_strength(new_password)
        self.password = self.hash_password(new_password)

    @classmethod
    def load_roles_from_yaml(cls, file_path=ROLES_FILE_PATH):
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
        cls.ROLES_AND_PERMISSIONS = data.get("roles", {})

    def has_permission(self, action, resource):
        role_permissions = self.ROLES_AND_PERMISSIONS.get(self.member_type, [])
        for permission in role_permissions:
            if permission["action"] == action and permission["resource"] == resource:
                return True
        return False
