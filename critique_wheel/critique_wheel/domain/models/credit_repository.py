import abc
from typing import List, Optional
from uuid import UUID

from critique_wheel.domain.models.credit import CreditManager


class AbstractCreditRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, credit: CreditManager) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, transaction_id: UUID) -> Optional[CreditManager]:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[CreditManager]:
        raise NotImplementedError
