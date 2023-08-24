from sqlalchemy.orm import Session
from typing import Optional
from critique_wheel.domain.models.rating import Rating
from critique_wheel.domain.models.rating_repository import AbstractRatingRepository

class SqlAlchemyRatingRepository(AbstractRatingRepository):

    def __init__(self, session: Session):
        self.session = session

    def add(self, rating: Rating) -> None:
        self.session.add(rating)

    def get(self, rating_id: str) -> Optional[Rating]:
        return self.session.query(Rating).filter_by(id=rating_id).one_or_none()

    def list(self) -> list[Rating]:
        return self.session.query(Rating).all()
