from sqlalchemy.orm import Session
from typing import Optional
from critique_wheel.domain.models.credit import CreditManager
from critique_wheel.domain.models.credit_repository import AbstractCreditRepository

class SqlAlchemyCreditRepository(AbstractCreditRepository):

    def __init__(self, session: Session):
        self.session = session

    def add(self, credit: CreditManager) -> None:
        self.session.add(credit)

    def get(self, credit_id: str) -> Optional[CreditManager]:
        return self.session.query(CreditManager).filter_by(id=credit_id).one_or_none()

    def list(self) -> list[CreditManager]:
        return self.session.query(CreditManager).all()