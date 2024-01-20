from typing import Optional

from sqlalchemy.orm import Session

from critique_wheel.ratings.models.rating import Rating
from critique_wheel.ratings.models.rating_repository import AbstractRatingRepository
from critique_wheel.ratings.value_objects import RatingId


class RatingRepository(AbstractRatingRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, rating: Rating) -> None:
        self.session.add(rating)

    def get(self, rating_id: RatingId) -> Optional[Rating]:
        return self.session.query(Rating).filter_by(id=rating_id).one_or_none()

    def list(self) -> list[Rating]:
        return self.session.query(Rating).all()
