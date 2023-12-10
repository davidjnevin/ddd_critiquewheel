import logging
from typing import Optional

from critique_wheel.critiques.models.critique import Critique
from critique_wheel.members.exceptions import exceptions
from critique_wheel.members.models.IAM import Member
from critique_wheel.members.models.iam_repository import AbstractMemberRepository
from critique_wheel.members.value_objects import MemberId
from critique_wheel.works.models.work import Work


class BaseIAMServiceError(Exception):
    pass


class InvalidCredentials(BaseIAMServiceError):
    pass


class MemberNotFoundException(BaseIAMServiceError):
    pass


class DuplicateEntryError(BaseIAMServiceError):
    pass


class InvalidEntryError(BaseIAMServiceError):
    pass


logger = logging.getLogger(__name__)


def create_member(
    username: str, email: str, password: str, repo: AbstractMemberRepository, session
) -> MemberId:
    new_member = Member.create(username, email, password)
    repo.add(new_member)
    session.commit()
    return new_member.id


def login_member(
    email: str, password: str, repo: AbstractMemberRepository, session
) -> Member:
    try:
        member = repo.get_member_by_email(email)
    except exceptions.BaseIAMDomainError as e:
        logger.exception(f"An error occurred while logging in: {e}")
        raise InvalidCredentials("Invalid credentials")
    if member and member.verify_password(password):
        session.commit()
        return member
    else:
        raise InvalidCredentials("Invalid credentials")


def register_member(
    username: str,
    email: str,
    password: str,
    confirm_password: str,
    repo: AbstractMemberRepository,
    session,
) -> Member:
    check_for_unique_parameters(username, email, repo)
    new_member = Member.register(username, email, password, confirm_password)
    repo.add(new_member)
    session.commit()
    return new_member


def check_for_unique_parameters(
    username: str, email: str, repo: AbstractMemberRepository
) -> None:
    if repo.get_member_by_email(email):
        raise DuplicateEntryError("Email already in use")
    if repo.get_member_by_username(username):
        raise DuplicateEntryError("Email already in use")


def list_members(repo) -> list[Member]:
    return repo.list()


def get_member_by_username(
    username: str, repo: AbstractMemberRepository
) -> Optional[Member]:
    return repo.get_member_by_username(username)


def get_member_by_id(
    member_id: str, repo: AbstractMemberRepository
) -> Optional[Member]:
    return repo.get_member_by_id(MemberId.from_string(uuid_string=member_id))


def list_member_works(
    member_id: MemberId, repo: AbstractMemberRepository
) -> list[Work]:
    member = repo.get_member_by_id(member_id)  # type: ignore
    if member:
        return member.list_works()
    else:
        raise MemberNotFoundException("Member not found")


def list_member_critiques(
    member_id: MemberId, repo: AbstractMemberRepository
) -> list[Critique]:
    member = repo.get_member_by_id(member_id)
    if member:
        return member.list_critiques()
    else:
        raise MemberNotFoundException("Member not found")
