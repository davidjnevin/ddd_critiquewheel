from typing import Optional

from sqlalchemy.orm import Session

from critique_wheel.credits.models.credit import CreditManager
from critique_wheel.credits.models.credit_repository import AbstractCreditRepository
from critique_wheel.credits.value_objects import TransactionId


class CreditRepository(AbstractCreditRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, credit: CreditManager) -> None:
        self.session.add(credit)

    def get(self, transaction_id: TransactionId) -> Optional[CreditManager]:
        return (
            self.session.query(CreditManager).filter_by(id=transaction_id).one_or_none()
        )

    def list(self) -> list[CreditManager]:
        return self.session.query(CreditManager).all()
