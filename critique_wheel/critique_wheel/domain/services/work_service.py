from sqlalchemy import UUID

from critique_wheel.domain.models.critique import Critique
from critique_wheel.domain.models.IAM import Member
from critique_wheel.domain.models.work import Work, WorkAgeRestriction, WorkGenre
from critique_wheel.domain.models.work_repository import AbstractWorkRepository


class WorkNotFoundException(Exception):
    pass


class DuplicateWorkError(Exception):
    pass


class WorkService:
    def __init__(self, repository: AbstractWorkRepository):
        self._repository = repository

    def create_work(
        self,
        title,
        content,
        member_id,
        genre=WorkGenre.OTHER,
        age_restriction=WorkAgeRestriction.ADULT,
        critiques=None,
    ) -> Work:
        new_work = Work.create(
            title=title,
            content=content,
            age_restriction=age_restriction,
            genre=genre,
            member_id=member_id,
            critiques=critiques,
        )
        self._repository.add(new_work)
        return new_work

    def list_works(self) -> list[Work]:
        return self._repository.list()

    def get_work_by_id(self, work_id: UUID) -> Work:
        work = self._repository.get_work_by_id(work_id)
        if work:
            return work
        else:
            raise WorkNotFoundException("Work not found")
