
from sqlalchemy import UUID
from critique_wheel.domain.models.work import Work, WorkNotFoundException
from critique_wheel.domain.models.work_repository import AbstractWorkRepository

class FakeWorkRepository(AbstractWorkRepository):
    def __init__(self, works: list[Work]):
        self._works = set(works)

    def add(self, work: Work) -> None:
        self._works.add(work)

    def get_work_by_id(self, work_id: UUID) -> Optional[Member]:
        try:
            return next(w for w in self._works if w.id == work_id)
        except StopIteration:
            raise WorkNotFoundException("Not found")

    def get_work_by_member_id(self, member_id: UUID) -> Optional[Work]:
        try:
            return next(w for w in self._works if w.member_id == member_id)
        except StopIteration:
            raise WorkNotFoundException("Not found")

    def list(self) -> list[Work]:
        return list(self._works)
