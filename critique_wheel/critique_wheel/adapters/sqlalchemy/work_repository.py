import logging
from typing import Optional

from sqlalchemy.orm import Session

from critique_wheel.members.value_objects import MemberId
from critique_wheel.works.models.work import Work
from critique_wheel.works.models.work_repository import AbstractWorkRepository
from critique_wheel.works.value_objects import WorkId

logger = logging.getLogger(__name__)


class WorkRepository(AbstractWorkRepository):
    def __init__(self, session: Session):
        logger.debug("Creating work repository.")
        self.session = session

    def add(self, work: Work) -> None:
        logger.debug(f"Adding work: {work}")
        self.session.add(work)

    def get_work_by_id(self, work_id: WorkId) -> Optional[Work]:
        logger.debug(f"Getting work by id: {work_id}")
        return self.session.query(Work).filter_by(id=str(work_id)).one_or_none()

    def get_work_by_member_id(self, member_id: MemberId) -> Optional[Work]:
        logger.debug(f"Getting work by member id: {member_id}")
        return (
            self.session.query(Work).filter_by(member_id=str(member_id)).one_or_none()
        )

    def list(self) -> list[Work]:
        logger.debug("Getting all works.")
        return self.session.query(Work).all()
