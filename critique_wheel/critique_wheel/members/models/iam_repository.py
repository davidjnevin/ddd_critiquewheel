import abc
from typing import List, Optional

from critique_wheel.members.models.IAM import Member
from critique_wheel.members.value_objects import MemberId


class AbstractMemberRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, member: Member) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_member_by_id(self, member_id: MemberId) -> Optional[Member]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_member_by_email(self, email: str) -> Optional[Member]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_member_by_username(self, username: str) -> Optional[Member]:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[Member]:
        raise NotImplementedError
