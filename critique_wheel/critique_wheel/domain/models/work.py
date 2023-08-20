import uuid
from datetime import datetime
from enum import Enum


class MissingEntryError(Exception):
    pass

class WorkNotAvailableForCritique(Exception):
    pass

class WorkStatus(str, Enum):
    PENDING_REVIEW = "Pending Review"
    ACTIVE = "Active"
    REJECTED = "Rejected"
    ARCHIVED = "Archived"
    MARKED_FOR_DELETION = "Marked for Deletion"


class WorkAgeRestriction(str, Enum):
    NONE = "None"
    TEEN = "Teen"
    ADULT = "Adult"


class WorkGenre(str, Enum):
    BIOGRAPHY = "Biography"
    CHICKLIT = "Chicklit"
    CHILDREN = "Children"
    COMEDY = "Comedy"
    CRIME = "Crime"
    DRAMA = "Drama"
    FANTASY = "Fantasy"
    HISTORICALFICTION = "Historical Fiction"
    HORROR = "Horror"
    LITERARY = "Literary"
    MYSTERY = "Mystery"
    NEWADULT = "New Adult"
    PARANORMAL = "Paranormal"
    ROMANCE = "Romance"
    SCIENCEFICTION = "Science Fiction"
    SPECULATIVE = "Speculative"
    SUSPENSE = "Suspense"
    THRILLER = "Thriller"
    UNDECIDED = "Undecided"
    URBANFANTASY = "Urban Fantasy"
    WOMENSLIT = "Womens Lit"
    YOUNGADULT = "Young Adult"
    OTHER = "Other"


class Work:
    def __init__(
        self,
        title,
        content,
        status=WorkStatus.PENDING_REVIEW,
        age_restriction=WorkAgeRestriction.ADULT,
        work_id=None,
        genre=WorkGenre.OTHER,
    ) -> None:
        self.id = work_id or uuid.uuid4()
        self.title: str = title
        self.content: str = content
        self.age_restriction: WorkAgeRestriction = age_restriction
        self.genre: WorkGenre = genre
        self.status: WorkStatus = status
        self.word_count: int = len(content.split())
        self.submission_date: datetime = datetime.now()
        self.last_update_date: datetime = datetime.now()
        self.archive_date = None

    @classmethod
    def create(
        cls,
        title,
        content,
        age_restriction,
        genre,
        status=WorkStatus.PENDING_REVIEW,
    ):
        if not title or not content:
            raise MissingEntryError()
        if not genre or not age_restriction:
            raise MissingEntryError()
        return cls(title, content, status, age_restriction, genre)

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
