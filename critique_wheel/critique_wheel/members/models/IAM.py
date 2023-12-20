import logging
import os
import random
import string
from datetime import datetime
from enum import Enum

import bcrypt
import yaml
from dotenv import load_dotenv

from critique_wheel.members.exceptions import exceptions
from critique_wheel.members.value_objects import MemberId

logger = logging.getLogger(__name__)
load_dotenv()

ROLES_FILE_PATH = os.getenv("ROLES_FILE_PATH")

assert os.path.exists(ROLES_FILE_PATH), f"File not found at {ROLES_FILE_PATH}"  # type: ignore
# Mock database to facilitate testing and building domain logic without a database
mock_db = {}
bcrypt.gensalt(rounds=4)  # Set the number of rounds for testing to 4


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
        self.id = member_id or MemberId()
        self.username: str = username
        self.email: str = email
        self.password: str = password
        self.member_type: MemberRole = member_type
        self.status: MemberStatus = status
        self.works = works or []
        self.critiques = critiques or []
        self.last_login: datetime = datetime.now()
        self.last_updated_date: datetime = datetime.now()
        self.created_date: datetime = datetime.now()

    @staticmethod
    def hash_password(password: str) -> str:
        bcrypt.gensalt(rounds=4)  # Set the number of rounds for testing to 4
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password.decode("utf-8")

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
            raise exceptions.MissingEntryError("Missing required fields")
        return cls(
            username=username,
            email=email,
            password=hashed_password,
            member_type=member_type,
            status=status,
            works=works or [],
            critiques=critiques or [],
        )

    def to_dict(self) -> dict:
        logger.debug("Converting member to dict.")
        return {
            "id": str(self.id),
            "username": str(self.username),
            "email": str(self.email),
            "password": str(self.password),
            "member_type": str(self.member_type.value),
            "status": str(self.status.value),
            "works": [str(work) for work in self.works],
            "critiques": [str(critique) for critique in self.critiques],
            "last_login": self.last_login.isoformat(),
            "last_updated_date": self.last_updated_date.isoformat(),
            "created_date": self.created_date.isoformat(),
        }

    @classmethod
    def register(cls, username, email, password, confirm_password):
        cls._validate_registration_parameters(
            username, email, password, confirm_password
        )
        try:
            cls.validate_password_strength(password)
        except exceptions.WeakPasswordError as e:
            logger.exception(f"Password does not meet the policy requirements {e}")
            raise exceptions.WeakPasswordError(
                "Password does not meet the policy requirements"
            )
        member = cls.create(username, email, password)
        return member

    @staticmethod
    def validate_password_strength(password: str):
        if len(password) < 8:
            raise exceptions.WeakPasswordError(
                "Password does not meet the policy requirements: Minimum length of 8 characters required."
            )
        if password.isalpha() or password.isdigit() or password.isalnum():
            raise exceptions.WeakPasswordError(
                "Password does not meet the policy requirements: Mix of letters, numbers, and symbols required."
            )
        for word in ["password", "abcdefg", "12345678", "qwerty"]:
            if word in password.lower():
                raise exceptions.WeakPasswordError(
                    "Password does not meet the policy requirements: Password is easily guessable."
                )

    @classmethod
    def _validate_registration_parameters(
        cls, username: str, email: str, password: str, confirm_password: str
    ) -> bool:
        if not username:
            raise exceptions.MissingEntryError("Missing required fields: username")
        if not email:
            raise exceptions.MissingEntryError("Missing required fields: email")
        if not password:
            raise exceptions.MissingEntryError("Missing required fields: password")
        if not confirm_password:
            raise exceptions.MissingEntryError(
                "Missing required fields: confirm password"
            )
        if password != confirm_password:
            raise exceptions.NonMatchingPasswordsError("Passwords do not match")
        return True

    def change_password(self, old_password, new_password):
        self.validate_password_strength(new_password)
        stored_password = self.password.encode()
        if not bcrypt.checkpw(old_password.encode(), stored_password):
            raise exceptions.IncorrectCredentialsError("Incorrect old password")
        self.password = self.hash_password(new_password)

    def verify_password(self, password):
        stored_password = self.password.encode()
        return bcrypt.checkpw(password.encode(), stored_password)

    def deactivate_self(self):
        self.status = MemberStatus.INACTIVE

    def deactivate_member(self, member):
        if self.member_type != MemberRole.ADMIN:
            raise exceptions.AdminOnlyError("Only admins can deactivate members.")
        member.status = MemberStatus.INACTIVE

    def generate_email_verification_code(self):
        # TODO: Implement email verification code generation
        return "".join(random.choices(string.ascii_letters + string.digits, k=6))

    def request_password_reset(self):
        # TODO: Implement token generation logic
        # For simplicity, we'll use a random string as the token.
        # In a real-world scenario, you'd want a more secure token generation mechanism.
        token = "".join(random.choices(string.ascii_letters + string.digits, k=32))
        # TODO: Store the token in the database with an expiration time
        # TODO: Send the token via the Notification Context
        return token

    # TODO: Implement the reset_password method in service layer
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

    def list_critiques(self) -> list:
        return self.critiques

    def add_critique(self, critique) -> None:
        if critique not in self.critiques:
            self.critiques.append(critique)
            self.last_update_date = datetime.now()
        else:
            raise exceptions.CritiqueAlreadyExistsError("Critique already exists")
