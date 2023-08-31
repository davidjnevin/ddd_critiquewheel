from typing import Optional

from sqlalchemy import UUID

from critique_wheel.domain.models.IAM import Member
from critique_wheel.domain.models.iam_repository import AbstractMemberRepository
from critique_wheel.domain.services.iam_service import (
    MemberNotFoundException,
)


class FakeMemberRepository(AbstractMemberRepository):
    def __init__(self, members: list[Member]):
        self._members = set(members)

    def add(self, member: Member) -> None:
        self._members.add(member)

    def get_member_by_id(self, member_id: UUID) -> Optional[Member]:
        try:
            return next(m for m in self._members if m.id == member_id)
        except StopIteration:
            raise MemberNotFoundException("Not found")

    def get_member_by_email(self, email: str) -> Optional[Member]:
        try:
            return next(m for m in self._members if m.email == email)
        except StopIteration:
            raise MemberNotFoundException("Not found")

    def get_member_by_username(self, username: str) -> Optional[Member]:
        try:
            return next(m for m in self._members if m.username == username)
        except StopIteration:
            raise MemberNotFoundException("Not found")

    def list(self) -> list[Member]:
        return list(self._members)
