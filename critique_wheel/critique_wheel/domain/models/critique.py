
from uuid import uuid4, UUID
from datetime import datetime
from enum import Enum


class MissingEntryError(Exception):
    pass


class CritiqueStatus(str, Enum):
    PENDING_REVIEW = "Pending Review"
    ACTIVE = "Active"
    REJECTED = "Rejected"
    ARCHIVED = "Archived"
    MARKED_FOR_DELETION = "Marked for Deletion"


class Critique:
    def __init__(
        self,
        content_about,
        content_successes,
        content_weaknesses,
        content_ideas,
        member_id,
        work_id,
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

    @classmethod
    def create(
        cls,
        content_about,
        content_successes,
        content_weaknesses,
        content_ideas,
        member_id,
        work_id,
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

