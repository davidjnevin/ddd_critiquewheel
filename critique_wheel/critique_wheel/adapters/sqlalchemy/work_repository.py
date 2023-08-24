from sqlalchemy.orm import Session
from typing import Optional
from critique_wheel.domain.models.work import Work
from critique_wheel.domain.models.work_repository import AbstractWorkRepository

class SqlAlchemyWorkRepository(AbstractWorkRepository):

    def __init__(self, session: Session):
        self.session = session

    def add(self, work: Work) -> None:
        self.session.add(work)

    def get(self, work_id: str) -> Optional[Work]:
        return self.session.query(Work).filter_by(id=work_id).one_or_none()

    def list(self) -> list[Work]:
        return self.session.query(Work).all()
