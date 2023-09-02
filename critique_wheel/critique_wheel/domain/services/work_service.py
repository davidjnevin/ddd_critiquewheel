from typing import Optional
from sqlalchemy import UUID

from critique_wheel.domain.models.work import BaseWorkDomainError, Work, WorkAgeRestriction, WorkGenre
from critique_wheel.domain.models.work_repository import AbstractWorkRepository

class BaseWorkServiceError(Exception):
    pass

class DuplicateWorkError(BaseWorkServiceError):
    pass

class InvalidDataError(BaseWorkServiceError):
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
        work_id=None,
    ) -> Work:
        try:
            new_work = Work.create(
                title=title,
                content=content,
                age_restriction=age_restriction,
                genre=genre,
                member_id=member_id,
                critiques=critiques,
                work_id=work_id,
            )
        except BaseWorkDomainError:
            raise InvalidDataError()
        if self._repository.get_work_by_id(new_work.id):
            raise DuplicateWorkError(f"Work with id {new_work.id} already exists")
        self._repository.add(new_work)
        return new_work

    def list_works(self) -> list[Work]:
        return self._repository.list()

    def get_work_by_id(self, work_id: UUID) -> Optional[Work]:
        return self._repository.get_work_by_id(work_id)
