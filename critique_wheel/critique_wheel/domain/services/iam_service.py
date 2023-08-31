from sqlalchemy import UUID

from critique_wheel.domain.models.critique import Critique
from critique_wheel.domain.models.IAM import Member
from critique_wheel.domain.models.iam_repository import AbstractMemberRepository
from critique_wheel.domain.models.work import Work


class MemberNotFoundException(Exception):
    pass


class MissingEntryError(Exception):
    pass


class InvalidCredentials(Exception):
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
        except MemberNotFoundException:
            raise InvalidCredentials("Invalid credentials")
        if member and member.verify_password(password):
            return member
        else:
            raise InvalidCredentials("Invalid credentials")

    def register_member(self, username: str, email: str, password: str, confirm_password: str) -> Member:
        if not username:
            raise MissingEntryError("Missing required fields: username")
        if not email:
            raise MissingEntryError("Missing required fields: email")
        if not password:
            raise MissingEntryError("Missing required fields: password")
        if not confirm_password:
            raise MissingEntryError("Missing required fields: confirm password")
        if password != confirm_password:
            raise InvalidCredentials("Passwords do not match")
        try:
            Member.validate_password_strength(password)
        except ValueError:
            # TODO: pass errors from model up to service
            raise InvalidCredentials("Password is weak")
        new_member = Member.create(username=username, email=email, password=password)
        self._repository.add(new_member)
        return new_member

    def list_members(self) -> list[Member]:
        return self._repository.list()

    def get_member_by_id(self, member_id: UUID) -> Member:
        member = self._repository.get(member_id)
        if member:
            return member
        else:
            raise MemberNotFoundException("Member not found")

    def add_work_to_member(self, member_id: UUID, work: Work) -> None:
        member = self._repository.get(member_id)
        if member:
            member.add_work(work)
            self._repository.add(member)
        else:
            raise MemberNotFoundException("Member not found")

    def add_critique_to_member(self, member_id: UUID, critique: Critique) -> None:
        member = self._repository.get(member_id)
        if member:
            member.add_critique(critique)
            self._repository.add(member)
        else:
            raise MemberNotFoundException("Member not found")

    def list_member_works(self, member_id: UUID) -> list[Work]:
        member = self._repository.get(member_id)  # type: ignore
        if member:
            return member.list_works()
        else:
            raise MemberNotFoundException("Member not found")

    def list_member_critiques(self, member_id: UUID) -> list[Critique]:
        member = self._repository.get(member_id)
        if member:
            return member.list_critiques()
        else:
            raise MemberNotFoundException("Member not found")
