from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class BaseWorkDomainError(Exception):
    pass


class MissingEntryError(BaseWorkDomainError):
    pass


class WorkNotAvailableForCritiqueError(BaseWorkDomainError):
    pass


class CritiqueDuplicateError(BaseWorkDomainError):
    pass


class WorkStatus(str, Enum):
    PENDING_REVIEW = "PENDING REVIEW"
    ACTIVE = "ACTIVE"
    REJECTED = "REJECTED"
    ARCHIVED = "ARCHIVED"
    MARKED_FOR_DELETION = "MARKED FOR DELETION"


class WorkAgeRestriction(str, Enum):
    NONE = "NONE"
    TEEN = "TEEN"
    ADULT = "ADULT"


class WorkGenre(str, Enum):
    BIOGRAPHY = "BIOGRAPHY"
    CHICKLIT = "CHICKLIT"
    CHILDREN = "CHILDREN"
    COMEDY = "COMEDY"
    CRIME = "CRIME"
    DRAMA = "DRAMA"
    FANTASY = "FANTASY"
    HISTORICALFICTION = "HISTORICAL FICTION"
    HORROR = "HORROR"
    LITERARY = "LITERARY"
    MYSTERY = "MYSTERY"
    NEWADULT = "NEW ADULT"
    PARANORMAL = "PARANORMAL"
    ROMANCE = "ROMANCE"
    SCIENCEFICTION = "SCIENCE FICTION"
    SPECULATIVE = "SPECULATIVE"
    SUSPENSE = "SUSPENSE"
    THRILLER = "THRILLER"
    UNDECIDED = "UNDECIDED"
    URBANFANTASY = "URBAN FANTASY"
    WOMENSLIT = "WOMENS LIT"
    YOUNGADULT = "YOUNG ADULT"
    OTHER = "OTHER"


class Work:
    def __init__(
        self,
        title,
        content,
        member_id,
        status=WorkStatus.PENDING_REVIEW,
        age_restriction=WorkAgeRestriction.ADULT,
        work_id=None,
        genre=WorkGenre.OTHER,
        critiques=None,
    ) -> None:
        self.id = work_id or uuid4()
        self.title: str = title
        self.content: str = content
        self.age_restriction: WorkAgeRestriction = age_restriction
        self.genre: WorkGenre = genre
        self.status: WorkStatus = status
        self.word_count: int = len(content.split())
        self.submission_date: datetime = datetime.now()
        self.last_update_date: datetime = datetime.now()
        self.archive_date = None
        self.member_id: UUID = member_id
        self.critiques = critiques or []

    @classmethod
    def create(
        cls,
        title,
        content,
        member_id,
        genre=WorkGenre.OTHER,
        age_restriction=WorkAgeRestriction.ADULT,
        critiques=None,
    ):
        if not title or not content:
            raise MissingEntryError()
        if not genre or not age_restriction or not member_id:
            raise MissingEntryError()
        return cls(
            title=title,
            content=content,
            age_restriction=age_restriction,
            genre=genre,
            member_id=member_id,
            critiques=critiques or [],
        )

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
            raise WorkNotAvailableForCritiqueError(
                "This work is not available for critique",
            )
        if critique not in self.critiques:
            self.critiques.append(critique)
            self.last_update_date = datetime.now()
        else:
            raise CritiqueDuplicateError("Critique already exists")
