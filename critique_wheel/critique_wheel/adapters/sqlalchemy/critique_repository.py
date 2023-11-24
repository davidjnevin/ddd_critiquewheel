from typing import Optional

from sqlalchemy.orm import Session

from critique_wheel.domain.models.critique import Critique
from critique_wheel.domain.models.critique_repository import AbstractCritiqueRepository


class SqlAlchemyCritiqueRepository(AbstractCritiqueRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, critique: Critique) -> None:
        self.session.add(critique)

    def get(self, critique_id: str) -> Optional[Critique]:
        return self.session.query(Critique).filter_by(id=critique_id).one_or_none()

    def list(self) -> list[Critique]:
        return self.session.query(Critique).all()
