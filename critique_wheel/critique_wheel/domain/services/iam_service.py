from typing import Optional
from sqlalchemy import UUID

from critique_wheel.domain.models.critique import Critique
from critique_wheel.domain.models.IAM import Member
from critique_wheel.domain.models.IAM_domain_exceptions import BaseIAMDomainError
from critique_wheel.domain.models.iam_repository import AbstractMemberRepository
from critique_wheel.domain.models.work import Work


class BaseIAMServiceError(Exception):
    pass


class InvalidCredentials(BaseIAMServiceError):
    pass


class MemberNotFoundException(BaseIAMServiceError):
    pass


class DuplicateEntryError(BaseIAMServiceError):
    pass


class IAMService:
    def __init__(self, repository: AbstractMemberRepository):
        self._repository = repository

    def create_member(self, username: str, email: str, password: str) -> Member:
        new_member = Member.create(username=username, email=email, password=password)
        self._repository.add(new_member)
        return new_member

    def login_member(self, email: str, password: str) -> Member:
        try:
            member = self._repository.get_member_by_email(email)
        except BaseIAMDomainError as e:
            raise InvalidCredentials("Invalid credentials")
        if member and member.verify_password(password):
            return member
        else:
            raise InvalidCredentials("Invalid credentials")

    def register_member(
        self,
        username: str,
        email: str,
        password: str,
        confirm_password: str,
    ) -> Member:
        self.check_for_unique_parameters(username, email)
        new_member = Member.register(username, email, password, confirm_password)
        self._repository.add(new_member)
        return new_member

    def list_members(self) -> list[Member]:
        return self._repository.list()

    def get_member_by_username(self, username: str) -> Optional[Member]:
        return self._repository.get_member_by_username(username)

    def get_member_by_id(self, member_id: UUID) -> Optional[Member]:
        return self._repository.get_member_by_id(member_id)

    # This was added here because the since each
    # Work has a member_id and is closely related to a Member,
    def add_work_to_member(self, member_id: UUID, work: Work) -> None:
        member = self._repository.get_member_by_id(member_id)
        if member:
            member.add_work(work)
            self._repository.add(member)
        else:
            raise MemberNotFoundException("Member not found")

    # This was added here because the since each
    # critique has a member_id and is closely related to a Member,
    def add_critique_to_member(self, member_id: UUID, critique: Critique) -> None:
        member = self._repository.get_member_by_id(member_id)
        if member:
            member.add_critique(critique)
            self._repository.add(member)
        else:
            raise MemberNotFoundException("Member not found")

    def list_member_works(self, member_id: UUID) -> list[Work]:
        member = self._repository.get_member_by_id(member_id)  # type: ignore
        if member:
            return member.list_works()
        else:
            raise MemberNotFoundException("Member not found")

    def list_member_critiques(self, member_id: UUID) -> list[Critique]:
        member = self._repository.get_member_by_id(member_id)
        if member:
            return member.list_critiques()
        else:
            raise MemberNotFoundException("Member not found")

    def check_for_unique_parameters(self, username: str, email: str) -> None:
        if self._repository.get_member_by_email(email):
            raise DuplicateEntryError("Email already in use")
        if self._repository.get_member_by_username(username):
            raise DuplicateEntryError("Email already in use")
