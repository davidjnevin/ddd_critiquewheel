import logging

from critique_wheel.critiques.models.critique import Critique
from critique_wheel.members.models import IAM as model
from critique_wheel.members.models import exceptions as domain_exceptions
from critique_wheel.members.models.iam_repository import AbstractMemberRepository
from critique_wheel.members.services import exceptions as service_exceptions
from critique_wheel.members.services import unit_of_work as uow
from critique_wheel.members.value_objects import MemberId
from critique_wheel.works.models.work import Work

logger = logging.getLogger(__name__)


def add_member(
    uow: uow.AbstractUnitOfWork,
    username: str,
    email: str,
    password: str,
) -> dict:
    with uow:
        try:
            new_member = model.Member.create(
                username=username,
                email=email,
                password=password,
            )
            if uow.members.get_member_by_email(email):
                raise service_exceptions.DuplicateEntryError("Email already in use")
                logger.exception("An error occurred while creating a member.")
            uow.members.add(new_member)
            uow.commit()
            return new_member.to_dict()
        except domain_exceptions.InvalidEntryError as e:
            logger.exception(f"An error occurred while creating a member: {e}")
            raise service_exceptions.InvalidEntryError("Invalid entry")
        except domain_exceptions.IncorrectCredentialsError as e:
            logger.exception(f"An error occurred while creating a member: {e}")
            raise service_exceptions.InvalidCredentialsError("Invalid entry") from e


def login_member(
    uow: uow.AbstractUnitOfWork,
    email: str,
    password: str,
) -> dict:
    with uow:
        try:
            member = uow.members.get_member_by_email(email)
        except domain_exceptions.BaseIAMDomainError as e:
            logger.exception(f"An error occurred while logging in: {e}")
            raise service_exceptions.InvalidCredentialsError("Invalid credentials")
        if member and member.verify_password(password):
            uow.commit()
            return member.to_dict()
        else:
            raise service_exceptions.InvalidCredentialsError("Invalid credentials")


def register_member(
    uow: uow.AbstractUnitOfWork,
    username: str,
    email: str,
    password: str,
    confirm_password: str,
) -> dict:
    if not password:
        raise service_exceptions.MissingPasswordError("Missing password")
    if password != confirm_password:
        raise service_exceptions.PasswordMismatchError(
            "Password and confirm password do not match"
        )
    if not username:
        raise service_exceptions.MissingUsernameError("Missing username")
    if not email:
        raise service_exceptions.MissingEmailError("Missing email")
    with uow:
        try:
            try:
                check_for_unique_parameters(username, email, uow.members)
            except service_exceptions.DuplicateEntryError as e:
                logger.exception(f"An error occurred while registering a member: {e}")
                raise
            except service_exceptions.DuplicateUsernameError as e:
                logger.exception(f"An error occurred while registering a member: {e}")
                raise
            new_member = model.Member.register(
                username, email, password, confirm_password
            )
            uow.members.add(new_member)
            uow.commit()
            return new_member.to_dict()
        except domain_exceptions.BaseIAMDomainError as e:
            logger.exception(f"An error occurred while registering a member: {e}")
            raise service_exceptions.InvalidEntryError(f"Invalid entry: {e}")


def check_for_unique_parameters(
    username: str, email: str, repo: AbstractMemberRepository
) -> None:
    if repo.get_member_by_email(email):
        raise service_exceptions.DuplicateEntryError("Email already in use")
    if repo.get_member_by_username(username):
        raise service_exceptions.DuplicateUsernameError("Username already in use")


def list_members(uow: uow.AbstractUnitOfWork) -> list[model.Member]:
    with uow:
        return uow.members.list()


def get_member_by_username(username: str, uow: uow.AbstractUnitOfWork) -> model.Member:
    with uow:
        member = uow.members.get_member_by_username(username)
        if member:
            return member
        else:
            raise service_exceptions.MemberNotFoundError("Member not found")


def get_member_by_id(member_id: MemberId, uow: uow.AbstractUnitOfWork) -> model.Member:
    member = uow.members.get_member_by_id(member_id)
    if member:
        return member
    else:
        raise service_exceptions.MemberNotFoundError("Member not found")


def list_member_works(member_id: MemberId, uow: uow.AbstractUnitOfWork) -> list[Work]:
    member = uow.members.get_member_by_id(member_id)  # type: ignore
    if member:
        return member.list_works()
    else:
        raise service_exceptions.MemberNotFoundException("Member not found")


def list_member_critiques(
    member_id: MemberId, uow: uow.AbstractUnitOfWork
) -> list[Critique]:
    member = uow.members.get_member_by_id(member_id)
    if member:
        return member.list_critiques()
    else:
        raise service_exceptions.MemberNotFoundException("Member not found")
