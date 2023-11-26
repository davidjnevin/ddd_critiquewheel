import abc
from typing import List, Optional

from critique_wheel.members.value_objects import MemberId
from critique_wheel.works.models.work import Work
from critique_wheel.works.value_objects import WorkId


class AbstractWorkRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, work: Work) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_work_by_id(self, work_id: WorkId) -> Optional[Work]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_work_by_member_id(self, member_id: MemberId) -> Optional[Work]:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[Work]:
        raise NotImplementedError
