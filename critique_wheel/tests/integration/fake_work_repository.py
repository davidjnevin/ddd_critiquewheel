import logging
from typing import Optional

from critique_wheel.members.value_objects import MemberId
from critique_wheel.works.models.work import Work
from critique_wheel.works.models.work_repository import AbstractWorkRepository
from critique_wheel.works.value_objects import WorkId

logger = logging.getLogger(__name__)


class FakeWorkRepository(AbstractWorkRepository):
    def __init__(self, works: list[Work]):
        self._works = set(works)
        self.committed = False

    def add(self, work: Work) -> None:
        self._works.add(work)

    def get_work_by_id(self, work_id: WorkId) -> Optional[Work]:
        try:
            return next(w for w in self._works if w.id == work_id)
        except StopIteration:
            logger.exception(f"Work with id {str(work_id)} not found")
            return None

    def get_work_by_member_id(self, member_id: MemberId) -> Optional[Work]:
        try:
            return next(w for w in self._works if w.member_id == member_id)
        except StopIteration:
            logger.exception(f"Work with member id {str(member_id)} not found")
            return None

    def list(self) -> list[Work]:
        return list(self._works)

    def commit(self) -> None:
        self.committed = True
