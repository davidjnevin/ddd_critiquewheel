import abc
from typing import List, Optional
from uuid import UUID
from critique_wheel.domain.models.work import Work

class AbstractWorkRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, work: Work) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_work_by_id(self, work_id: UUID) -> Optional[Work]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_work_by_member_id(self, member_id: UUID) -> Optional[Work]:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[Work]:
        raise NotImplementedError
