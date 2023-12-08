import logging
from typing import Optional

from critique_wheel.critiques.models.critique import Critique
from critique_wheel.members.exceptions import exceptions
from critique_wheel.members.models.IAM import Member
from critique_wheel.members.models.iam_repository import AbstractMemberRepository
from critique_wheel.members.value_objects import MemberId
from critique_wheel.works.models.work import Work
from critique_wheel.works.models.work_repository import AbstractWorkRepository
from critique_wheel.works.services import work_service
from critique_wheel.works.value_objects import WorkId


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
    check_for_unique_parameters(username, email, repo, session)
    new_member = Member.register(username, email, password, confirm_password)
    repo.add(new_member)
    session.commit()
    return new_member


def check_for_unique_parameters(
    username: str, email: str, repo: AbstractMemberRepository, session
) -> None:
    if repo.get_member_by_email(email):
        raise DuplicateEntryError("Email already in use")
    if repo.get_member_by_username(username):
        raise DuplicateEntryError("Email already in use")


def list_members(repo, session) -> list[Member]:
    return repo.list()


def get_member_by_username(
    username: str, repo: AbstractMemberRepository
) -> Optional[Member]:
    return repo.get_member_by_username(username)


def get_member_by_id(
    member_id: str, repo: AbstractMemberRepository
) -> Optional[Member]:
    return repo.get_member_by_id(MemberId.from_string(uuid_string=member_id))


# This was added here because each Work
# has a member_id and is closely related to a Member,
def add_work_to_member(
    member_id: str,
    work_id: str,
    repo: AbstractMemberRepository,
    work_repo: AbstractWorkRepository,
    session,
) -> None:
    try:
        workId = WorkId.from_string(uuid_string=work_id)
    except exceptions.MissingEntryError as e:
        logger.exception(f"An error occurred while adding work to member: {e}")
        raise work_service.WorkNotFoundError(f"Invalid data encountered: {e}") from e
    try:
        memberId = MemberId.from_string(uuid_string=member_id)
    except exceptions.InvalidEntryError as e:
        logger.exception(f"An error occurred while adding work to member: {e}")
        raise MemberNotFoundException(f"Invalid data encountered: {e}") from e

    work = work_repo.get_work_by_id(workId)
    member = repo.get_member_by_id(memberId)

    if member and work:
        member.add_work(work)
        repo.add(member)
        session.commit()
    else:
        raise InvalidEntryError("Member not found")


class IAMService:
    def __init__(self, repository: AbstractMemberRepository):
        self._repository = repository

    # This was added here because the since each
    # critique has a member_id and is closely related to a Member,
    def add_critique_to_member(self, member_id: MemberId, critique: Critique) -> None:
        member = self._repository.get_member_by_id(member_id)
        if member:
            member.add_critique(critique)
            self._repository.add(member)
        else:
            raise MemberNotFoundException("Member not found")

    def list_member_works(self, member_id: MemberId) -> list[Work]:
        member = self._repository.get_member_by_id(member_id)  # type: ignore
        if member:
            return member.list_works()
        else:
            raise MemberNotFoundException("Member not found")

    def list_member_critiques(self, member_id: MemberId) -> list[Critique]:
        member = self._repository.get_member_by_id(member_id)
        if member:
            return member.list_critiques()
        else:
            raise MemberNotFoundException("Member not found")
