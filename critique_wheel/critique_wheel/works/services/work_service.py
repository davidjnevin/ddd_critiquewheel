from typing import Optional

from critique_wheel.members.value_objects import MemberId
from critique_wheel.works.exceptions import exceptions
from critique_wheel.works.models.work import Work
from critique_wheel.works.models.work_repository import AbstractWorkRepository
from critique_wheel.works.value_objects import Content, Title, WorkId


class BaseWorkServiceError(Exception):
    pass


class DuplicateWorkError(BaseWorkServiceError):
    pass


class WorkNotFoundError(BaseWorkServiceError):
    pass


class InvalidDataError(BaseWorkServiceError):
    pass


def add_work(
    repo: AbstractWorkRepository,
    session,
    title: str,
    content: str,
    member_id: str,
    genre,
    age_restriction,
    work_id: str = "",
    critiques=None,
) -> dict:
    try:
        new_work = Work.create(
            work_id=WorkId.from_string(uuid_string=work_id) or WorkId(),
            title=Title(title),
            content=Content(content),
            member_id=MemberId.from_string(uuid_string=member_id),
            age_restriction=age_restriction,
            genre=genre,
            critiques=critiques,
        )
    except exceptions.MissingEntryError as e:
        raise InvalidDataError(f"Invalid data encountered: {e}") from e
    except Exception as e:
        raise InvalidDataError(f"Invalid data encountered: {e}") from e
    if work_id:
        if repo.get_work_by_id(new_work.id):
            raise DuplicateWorkError(f"Work with id {str(new_work.id)} already exists")
    repo.add(new_work)
    session.commit()
    return new_work.to_dict()


def list_works(repo) -> list[Work]:
    return [work.to_dict() for work in repo.list()]


def get_work_by_id(work_id: str, repo: AbstractWorkRepository) -> Optional[dict]:
    work = repo.get_work_by_id(WorkId.from_string(uuid_string=work_id))
    return work.to_dict() if work else None
