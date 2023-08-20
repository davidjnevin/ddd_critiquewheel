from uuid import uuid4, UUID
from datetime import datetime
from enum import Enum


class MissingEntryError(Exception):
    pass


class RatingStatus(str, Enum):
    PENDING_REVIEW = "Pending Review"
    ACTIVE = "Active"
    REJECTED = "Rejected"
    ARCHIVED = "Archived"
    MARKED_FOR_DELETION = "Marked for Deletion"


class Rating:
    def __init__(
        self,
        score,
        comment,
        critique_id,
        member_id,
        status=RatingStatus.ACTIVE,
        rating_id = None,
    ) -> None:
        self.id = rating_id or uuid4()
        self.score: int = score
        self.comment: str = comment
        self.status: RatingStatus = status
        self.submission_date: datetime = datetime.now()
        self.last_updated_date: datetime = datetime.now()
        self.archive_date = None
        self._member_id= member_id
        self._critique_id= critique_id

    @classmethod
    def create(
        cls,
        score,
        comment,
        critique_id,
        member_id,
    ):
        if score not in range(1, 6):
            raise ValueError("Score must be between 1 and 5.")
        if not member_id or not critique_id:
            raise MissingEntryError()
        return cls(
        score=score,
        comment=comment,
        critique_id=critique_id,
        member_id=member_id,
        )

    @property
    def critique_id(self):
        return self._critique_id

    @critique_id.setter
    def critique_id(self, value):
        raise AttributeError("Can't set attribute")

    @property
    def member_id(self):
        return self._member_id

    @member_id.setter
    def member_id(self, value):
        raise AttributeError("Can't set attribute")

    def update_score(self, updated_score:int) -> None:
        self.score = updated_score
        self.last_updated_date = datetime.now()

    def add_comment(self, comment:str) -> None:
        self.comment = comment
        self.last_updated_date = datetime.now()

    def approve(self) -> None:
        self.status = RatingStatus.ACTIVE
        self.archive_date = datetime.now()

    def reject(self) -> None:
        self.status = RatingStatus.REJECTED
        self.archive_date = datetime.now()

    def archive(self) -> None:
        self.status = RatingStatus.ARCHIVED
        self.archive_date = datetime.now()

    def mark_for_deletion(self) -> None:
        self.status = RatingStatus.MARKED_FOR_DELETION
        self.last_update_date = datetime.now()

    def mark_pending_review(self) -> None:
        self.status = RatingStatus.PENDING_REVIEW
        self.last_update_date = datetime.now()

    def restore(self) -> None:
        self.status = RatingStatus.ACTIVE
        self.archive_date = None
        self.last_update_date = datetime.now()

