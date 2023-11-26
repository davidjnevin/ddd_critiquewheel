from typing import Optional

from sqlalchemy.orm import Session

from critique_wheel.critiques.models.critique import Critique
from critique_wheel.critiques.models.critique_repository import (
    AbstractCritiqueRepository,
)
from critique_wheel.critiques.value_objects import CritiqueId


class SqlAlchemyCritiqueRepository(AbstractCritiqueRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, critique: Critique) -> None:
        self.session.add(critique)

    def get(self, critique_id: CritiqueId) -> Optional[Critique]:
        return self.session.query(Critique).filter_by(id=critique_id).one_or_none()

    def list(self) -> list[Critique]:
        return self.session.query(Critique).all()
