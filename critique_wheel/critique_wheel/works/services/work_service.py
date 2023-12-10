import logging
from typing import Optional

from critique_wheel.members import value_objects as member_value_objects
from critique_wheel.works import value_objects
from critique_wheel.works.exceptions import exceptions
from critique_wheel.works.models import work as model
from critique_wheel.works.services import unit_of_work as uow

logger = logging.getLogger(__name__)


class BaseWorkServiceError(Exception):
    pass


class DuplicateWorkError(BaseWorkServiceError):
    pass


class WorkNotFoundError(BaseWorkServiceError):
    pass


class InvalidDataError(BaseWorkServiceError):
    pass


def add_work(
    uow: uow.AbstractUnitOfWork,
    title: str,
    content: str,
    member_id: str,
    genre: str,
    age_restriction: str,
    work_id: Optional[str] = "",
    critiques: Optional[list] = None,
) -> dict:
    with uow:
        try:
            new_work = model.Work.create(
                work_id=value_objects.WorkId.from_string(uuid_string=work_id)
                or value_objects.WorkId(),
                title=value_objects.Title(title),
                content=value_objects.Content(content),
                member_id=member_value_objects.MemberId.from_string(
                    uuid_string=member_id
                ),
                age_restriction=value_objects.find_agerestriction_by_value(
                    age_restriction
                ),
                genre=value_objects.find_genre_by_value(genre),
                critiques=critiques,
            )
        except exceptions.MissingEntryError as e:
            logger.exception(f"Missing entry encountered: {e}")
            raise InvalidDataError(f"Invalid data encountered: {e}") from e
        except Exception as e:
            logger.exception(f"Invalid data encountered: {e}")
            raise InvalidDataError(f"Invalid data encountered: {e}") from e
        if uow.works.get_work_by_id(new_work.id):
            raise DuplicateWorkError(f"Work with id {str(new_work.id)} already exists")
        uow.works.add(new_work)
        uow.commit()
    return new_work.to_dict()


def list_works(
    uow: uow.AbstractUnitOfWork,
) -> list[dict]:
    with uow:
        works = [work.to_dict() for work in uow.works.list()]
    return works


def get_work_by_id(work_id: str, uow: uow.AbstractUnitOfWork) -> Optional[dict]:
    with uow:
        work = uow.works.get_work_by_id(
            value_objects.WorkId.from_string(uuid_string=work_id)
        )
    return work.to_dict() if work else None
