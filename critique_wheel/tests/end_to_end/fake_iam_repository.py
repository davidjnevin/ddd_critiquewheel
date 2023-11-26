from typing import Optional

from critique_wheel.members.models.IAM import Member
from critique_wheel.members.models.iam_repository import AbstractMemberRepository
from critique_wheel.members.value_objects import MemberId


class FakeMemberRepository(AbstractMemberRepository):
    def __init__(self, members: list[Member]):
        self._members = set(members)
        self.committed = False

    def add(self, member: Member) -> None:
        self._members.add(member)

    def get_member_by_id(self, member_id: MemberId) -> Optional[Member]:
        for m in self._members:
            if m.id == member_id:
                return m
        return None

    def get_member_by_email(self, email: str) -> Optional[Member]:
        for m in self._members:
            if m.email == email:
                return m
        return None

    def get_member_by_username(self, username: str) -> Optional[Member]:
        for m in self._members:
            if m.username == username:
                return m
        return None

    def list(self) -> list[Member]:
        return list(self._members)

    def commit(self) -> None:
        self.committed = True
