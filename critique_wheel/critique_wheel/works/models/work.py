from datetime import datetime

from critique_wheel.members.value_objects import MemberId
from critique_wheel.works.exceptions import exceptions
from critique_wheel.works.value_objects import (
    Content,
    Title,
    WorkAgeRestriction,
    WorkGenre,
    WorkId,
    WorkStatus,
)


class Work:
    def __init__(
        self,
        title: Title,
        content: Content,
        member_id: MemberId,
        status=WorkStatus.PENDING_REVIEW,
        age_restriction=WorkAgeRestriction.ADULT,
        work_id: WorkId = WorkId(),
        genre: WorkGenre = WorkGenre.OTHER,
        critiques=None,
    ) -> None:
        self.id = work_id or WorkId()
        self.title: Title = title
        self.content: Content = content
        self.age_restriction: WorkAgeRestriction = age_restriction
        self.genre: WorkGenre = genre
        self.status: WorkStatus = status
        self.word_count: int = len(str(content).split())
        self.submission_date: datetime = datetime.now()
        self.last_update_date: datetime = datetime.now()
        self.archive_date = None
        self.member_id: MemberId = member_id
        self.critiques = critiques or []

    @classmethod
    def create(
        cls,
        title: Title,
        content: Content,
        member_id: MemberId,
        genre=WorkGenre.OTHER,
        age_restriction=WorkAgeRestriction.ADULT,
        critiques=None,
        work_id: WorkId = None,
    ):
        if not title or not content:
            raise exceptions.MissingEntryError()
        if not genre or not age_restriction or not member_id:
            raise exceptions.MissingEntryError()
        return cls(
            title=title,
            content=content,
            age_restriction=age_restriction,
            genre=genre,
            member_id=member_id,
            critiques=critiques or [],
            work_id=work_id,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "title": str(self.title),
            "content": str(self.content),
            "age_restriction": self.age_restriction.value,
            "genre": self.genre.value,
            "status": self.status.value,
            "word_count": self.word_count,
            "submission_date": self.submission_date.isoformat(),
            "last_update_date": self.last_update_date.isoformat(),
            "archive_date": self.archive_date.isoformat()
            if self.archive_date
            else None,
            "member_id": str(self.member_id),
            "critiques": [str(critique) for critique in self.critiques],
        }

    def approve(self) -> None:
        self.status = WorkStatus.ACTIVE
        self.archive_date = datetime.now()

    def reject(self) -> None:
        self.status = WorkStatus.REJECTED
        self.archive_date = datetime.now()

    def archive(self) -> None:
        self.status = WorkStatus.ARCHIVED
        self.archive_date = datetime.now()

    def mark_for_deletion(self) -> None:
        self.status = WorkStatus.MARKED_FOR_DELETION
        self.last_update_date = datetime.now()

    def restore(self) -> None:
        if self.status == WorkStatus.ARCHIVED:
            self.status = WorkStatus.ACTIVE
            self.archive_date = None
            self.last_update_date = datetime.now()

    def is_available_for_critique(self) -> bool:
        if self.status == WorkStatus.ACTIVE:
            return True
        return False

    def list_critiques(self) -> list:
        return self.critiques

    def add_critique(self, critique) -> None:
        if not self.is_available_for_critique():
            raise exceptions.WorkNotAvailableForCritiqueError(
                "This work is not available for critique",
            )
        if critique not in self.critiques:
            self.critiques.append(critique)
            self.last_update_date = datetime.now()
        else:
            raise exceptions.CritiqueDuplicateError("Critique already exists")
