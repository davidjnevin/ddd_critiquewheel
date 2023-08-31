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

assert os.path.exists(ROLES_FILE_PATH), f"File not found at {ROLES_FILE_PATH}"  # type: ignore
# Mock database to facilitate testing and building domain logic without a database
mock_db = {}
bcrypt.gensalt(rounds=4)  # Set the number of rounds for testing to 4


class MissingEntryError(Exception):
    pass


class MemberStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    MARKER_FOR_DELETION = "DELETED"


class MemberRole(str, Enum):
    ADMIN = "ADMIN"
    STAFF = "STAFF"
    MEMBER = "MEMBER"



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
        works=None,
        critiques=None,
    ):
        self.id = member_id or uuid4()
        self.username: str = username
        self.email: str = email
        self.password: bytes = password
        self.member_type: MemberRole = member_type
        self.status: MemberStatus = status
        self.works = works or []
        self.critiques = critiques or []
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
        status=MemberStatus.INACTIVE,
        works=None,
        critiques=None,
    ):
        cls.validate_password_strength(password)
        hashed_password = cls.hash_password(password)
        if not username or not email or not password:
            raise MissingEntryError("Missing required fields")
        return cls(
            username=username,
            email=email,
            password=hashed_password,
            member_type=member_type,
            status=status,
            works=works or [],
            critiques=critiques or [],
        )



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
        for word in ["password", "abcdefg", "12345678", "qwerty"]:
            if word in password.lower():
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

    def list_works(self) -> list:
        return self.works

    def add_work(self, work) -> None:
        if work not in self.works:
            self.works.append(work)
            self.last_update_date = datetime.now()
        else:
            raise ValueError("Work already exists")

    def list_critiques(self) -> list:
        return self.critiques

    def add_critique(self, critique) -> None:
        if critique not in self.critiques:
            self.critiques.append(critique)
            self.last_update_date = datetime.now()
        else:
            raise ValueError("Critique already exists")
