import abc
from typing import List, Optional
from uuid import UUID

from critique_wheel.domain.models.IAM import Member


class AbstractMemberRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, member: Member) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, member_id: UUID) -> Optional[Member]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_member_by_email(self, email: str) -> Optional[Member]:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[Member]:
        raise NotImplementedError
