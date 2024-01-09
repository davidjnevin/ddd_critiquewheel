import logging
from typing import Optional

from critique_wheel.critiques.models.critique import Critique
from critique_wheel.members.exceptions import exceptions
from critique_wheel.members.models import IAM as model
from critique_wheel.members.models.iam_repository import AbstractMemberRepository
from critique_wheel.members.services import unit_of_work as uow
from critique_wheel.members.value_objects import MemberId
from critique_wheel.works.models.work import Work

logger = logging.getLogger(__name__)


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


def add_member(
    uow: uow.AbstractUnitOfWork,
    username: str,
    email: str,
    password: str,
) -> str:
    with uow:
        try:
            new_member = model.Member.create(
                username=username,
                email=email,
                password=password,
            )
        except exceptions.MemberInvalidEntryError as e:
            logger.exception(f"An error occurred while creating a member: {e}")
            raise InvalidEntryError("Invalid entry")
        except exceptions.InvalidPasswordError as e:
            logger.exception(f"An error occurred while creating a member: {e}")
            raise InvalidEntryError("Invalid entry")
        if uow.members.get_member_by_email(email):
            raise DuplicateEntryError("Email already in use")
            logger.exception("An error occurred while creating a member.")
        uow.members.add(new_member)
    return new_member.id


def login_member(
    uow: uow.AbstractUnitOfWork,
    email: str,
    password: str,
) -> dict:
    with uow:
        try:
            member = uow.members.get_member_by_email(email)
        except exceptions.BaseIAMDomainError as e:
            logger.exception(f"An error occurred while logging in: {e}")
            raise InvalidCredentials("Invalid credentials")
        if member and member.verify_password(password):
            uow.commit()
            return member.to_dict()
        else:
            raise InvalidCredentials("Invalid credentials")


def register_member(
    uow: uow.AbstractUnitOfWork,
    username: str,
    email: str,
    password: str,
    confirm_password: str,
) -> dict:
    check_for_unique_parameters(username, email, uow.members)
    new_member = model.Member.register(username, email, password, confirm_password)
    uow.members.add(new_member)
    uow.commit()
    return new_member.to_dict()


def check_for_unique_parameters(
    username: str, email: str, repo: AbstractMemberRepository
) -> None:
    if repo.get_member_by_email(email):
        raise DuplicateEntryError("Email already in use")
    if repo.get_member_by_username(username):
        raise DuplicateEntryError("Email already in use")


def list_members(uow: uow.AbstractUnitOfWork) -> list[model.Member]:
    return uow.members.list()


def get_member_by_username(
    username: str, uow: uow.AbstractUnitOfWork
) -> Optional[model.Member]:
    return uow.members.get_member_by_username(username)


def get_member_by_id(
    member_id: str, uow: uow.AbstractUnitOfWork
) -> Optional[model.Member]:
    return uow.members.get_member_by_id(MemberId.from_string(uuid_string=member_id))


def list_member_works(member_id: MemberId, uow: uow.AbstractUnitOfWork) -> list[Work]:
    member = uow.members.get_member_by_id(member_id)  # type: ignore
    if member:
        return member.list_works()
    else:
        raise MemberNotFoundException("Member not found")


def list_member_critiques(
    member_id: MemberId, uow: uow.AbstractUnitOfWork
) -> list[Critique]:
    member = uow.members.get_member_by_id(member_id)
    if member:
        return member.list_critiques()
    else:
        raise MemberNotFoundException("Member not found")
