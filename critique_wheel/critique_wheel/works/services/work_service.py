from typing import Optional

from critique_wheel.members.value_objects import MemberId
from critique_wheel.works.models.work import Work
from critique_wheel.works.models.work_repository import AbstractWorkRepository
from critique_wheel.works.value_objects import (
    Content,
    MissingEntryError,
    Title,
    WorkAgeRestriction,
    WorkGenre,
    WorkId,
)


class BaseWorkServiceError(Exception):
    pass


class DuplicateWorkError(BaseWorkServiceError):
    pass


class InvalidDataError(BaseWorkServiceError):
    pass


def add_work(
    repo: AbstractWorkRepository,
    session,
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
        if repo.get_work_by_id(new_work.id):
            raise DuplicateWorkError(f"Work with id {str(new_work.id)} already exists")
    repo.add(new_work)
    session.commit()
    return new_work


def list_works(repo) -> list[Work]:
    return repo.list()


def get_work_by_id(work_id: WorkId, repo: AbstractWorkRepository) -> Optional[Work]:
    return repo.get_work_by_id(work_id)
