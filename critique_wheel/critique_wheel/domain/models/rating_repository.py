import abc
from typing import List, Optional
from uuid import UUID
from critique_wheel.domain.models.rating import Rating

class AbstractRatingRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, rating: Rating) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, rating_id: UUID) -> Optional[Rating]:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[Rating]:
        raise NotImplementedError
