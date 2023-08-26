from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class MissingEntryError(Exception):
    pass


class CritiqueStatus(str, Enum):
    PENDING_REVIEW = "PENDING REVIEW"
    ACTIVE = "ACTIVE"
    REJECTED = "REJECTED"
    ARCHIVED = "ARCHIVED"
    MARKED_FOR_DELETION = "MARKED FOR DELETION"


class Critique:
    def __init__(
        self,
        content_about,
        content_successes,
        content_weaknesses,
        content_ideas,
        member_id,
        work_id,
        ratings,
        status=CritiqueStatus.ACTIVE,
        critique_id=None,
    ) -> None:
        self.id = critique_id or uuid4()
        self.content_about: str = content_about
        self.content_successes: str = content_successes
        self.content_weaknesses: str = content_weaknesses
        self.content_ideas: str = content_ideas
        self.status: CritiqueStatus = status
        self.submission_date: datetime = datetime.now()
        self.last_updated_date: datetime = datetime.now()
        self.archive_date = None
        self.member_id: UUID = member_id
        self.work_id: UUID = work_id
        self.ratings = ratings or []

    @classmethod
    def create(
        cls,
        content_about,
        content_successes,
        content_weaknesses,
        content_ideas,
        member_id,
        work_id,
        critique_id=None,
        ratings=None,
    ):
        if not content_about or not content_successes or not content_weaknesses or not content_ideas:
            raise MissingEntryError()
        if not member_id or not work_id:
            raise MissingEntryError()
        return cls(
            content_about=content_about,
            content_successes=content_successes,
            content_weaknesses=content_weaknesses,
            content_ideas=content_ideas,
            member_id=member_id,
            work_id=work_id,
            critique_id=critique_id,
            ratings=ratings or [],
        )

    def approve(self) -> None:
        self.status = CritiqueStatus.ACTIVE
        self.archive_date = datetime.now()

    def reject(self) -> None:
        self.status = CritiqueStatus.REJECTED
        self.archive_date = datetime.now()

    def archive(self) -> None:
        self.status = CritiqueStatus.ARCHIVED
        self.archive_date = datetime.now()

    def mark_for_deletion(self) -> None:
        self.status = CritiqueStatus.MARKED_FOR_DELETION
        self.last_update_date = datetime.now()

    def pending_review(self) -> None:
        self.status = CritiqueStatus.PENDING_REVIEW
        self.last_update_date = datetime.now()

    def restore(self) -> None:
        if self.status == CritiqueStatus.ARCHIVED:
            self.status = CritiqueStatus.ACTIVE
            self.archive_date = None
            self.last_update_date = datetime.now()

    def list_ratings(self) -> list:
        return self.ratings

    def add_rating(self, rating) -> None:
        if rating not in self.ratings:
            self.ratings.append(rating)
            self.last_update_date = datetime.now()
        else:
            raise ValueError("Rating already exists")
