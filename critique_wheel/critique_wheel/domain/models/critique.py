from datetime import datetime

from critique_wheel.critiques.value_objects import (
    CritiqueAbout,
    CritiqueId,
    CritiqueIdeas,
    CritiqueStatus,
    CritiqueSuccesses,
    CritiqueWeaknesses,
    MissingEntryError,
)
from critique_wheel.members.value_objects import MemberId
from critique_wheel.works.value_objects import WorkId


class Critique:
    def __init__(
        self,
        critique_about,
        critique_successes,
        critique_weaknesses,
        critique_ideas,
        member_id,
        work_id,
        ratings,
        status=CritiqueStatus.ACTIVE,
        critique_id=None,
    ) -> None:
        self.id: CritiqueId = critique_id or CritiqueId()
        self.critique_about: CritiqueAbout = critique_about
        self.critique_successes: CritiqueSuccesses = critique_successes
        self.critique_weaknesses: CritiqueWeaknesses = critique_weaknesses
        self.critique_ideas: CritiqueIdeas = critique_ideas
        self.status: CritiqueStatus = status
        self.submission_date: datetime = datetime.now()
        self.last_updated_date: datetime = datetime.now()
        self.archive_date = None
        self.member_id: MemberId = member_id
        self.work_id: WorkId = work_id
        self.ratings = ratings or []

    @classmethod
    def create(
        cls,
        critique_about,
        critique_successes,
        critique_weaknesses,
        critique_ideas,
        member_id,
        work_id,
        critique_id=None,
        ratings=None,
    ):
        if (
            not critique_about
            or not critique_successes
            or not critique_weaknesses
            or not critique_ideas
        ):
            raise MissingEntryError()
        if not member_id or not work_id:
            raise MissingEntryError()
        if critique_about.is_minimum_word_length():
            raise ValueError(
                f"The about text should be at least {critique_about.minimum_words} words."
            )
        if critique_successes.is_minimum_word_length():
            raise ValueError(
                f"The successes text should be at least {critique_successes.minimum_words} words."
            )
        if critique_weaknesses.is_minimum_word_length():
            raise ValueError(
                f"The weaknesses text should be at least {critique_weaknesses.minimum_words} words."
            )
        if critique_ideas.is_minimum_word_length():
            raise ValueError(
                f"The ideas text should be at least {critique_ideas.minimum_words} words."
            )
        return cls(
            critique_about=critique_about,
            critique_successes=critique_successes,
            critique_weaknesses=critique_weaknesses,
            critique_ideas=critique_ideas,
            member_id=member_id,
            work_id=work_id,
            critique_id=critique_id,
            ratings=ratings or [],
        )

    def approve(self) -> None:
        self.status = CritiqueStatus.ACTIVE
        self.last_updated_date = datetime.now()

    def reject(self) -> None:
        self.status = CritiqueStatus.REJECTED
        self.last_updated_date = datetime.now()

    def archive(self) -> None:
        self.status = CritiqueStatus.ARCHIVED
        self.last_updated_date = datetime.now()
        self.archive_date = datetime.now()

    def mark_for_deletion(self) -> None:
        self.status = CritiqueStatus.MARKED_FOR_DELETION
        self.last_updated_date = datetime.now()

    def pending_review(self) -> None:
        self.status = CritiqueStatus.PENDING_REVIEW
        self.last_updated_date = datetime.now()

    def restore(self) -> None:
        if self.status == CritiqueStatus.ARCHIVED:
            self.status = CritiqueStatus.ACTIVE
            self.archive_date = None
            self.last_updated_date = datetime.now()

    def list_ratings(self) -> list:
        return self.ratings

    def add_rating(self, rating) -> None:
        if rating not in self.ratings:
            self.ratings.append(rating)
            self.last_updated_date = datetime.now()
        else:
            raise ValueError("Rating already exists")
