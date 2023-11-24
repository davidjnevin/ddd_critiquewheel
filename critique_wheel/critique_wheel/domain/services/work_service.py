from typing import Optional

from critique_wheel.domain.models.work import Work, WorkAgeRestriction, WorkGenre
from critique_wheel.domain.models.work_repository import AbstractWorkRepository
from critique_wheel.members.value_objects import MemberId
from critique_wheel.works.value_objects import Content, MissingEntryError, Title, WorkId


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
        title: Title,
        content: Content,
        member_id: MemberId,
        genre=WorkGenre.OTHER,
        age_restriction=WorkAgeRestriction.ADULT,
        critiques=None,
        work_id=None,
    ) -> Work:
        try:
            new_work = Work.create(
                work_id=work_id or WorkId(),
                title=title,
                content=content,
                age_restriction=age_restriction,
                genre=genre,
                member_id=member_id,
                critiques=critiques,
            )
        except MissingEntryError as e:
            raise InvalidDataError(f"Invalid data encountered: {e}") from e
        if work_id:
            if self._repository.get_work_by_id(new_work.id):
                raise DuplicateWorkError(f"Work with id {str(new_work.id)} already exists")
        self._repository.add(new_work)
        return new_work

    def list_works(self) -> list[Work]:
        return self._repository.list()

    def get_work_by_id(self, work_id: WorkId) -> Optional[Work]:
        return self._repository.get_work_by_id(work_id)
