import abc
from typing import List, Optional

from critique_wheel.ratings.models.rating import Rating
from critique_wheel.ratings.value_objects import RatingId


class AbstractRatingRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, rating: Rating) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, rating_id: RatingId) -> Optional[Rating]:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[Rating]:
        raise NotImplementedError
