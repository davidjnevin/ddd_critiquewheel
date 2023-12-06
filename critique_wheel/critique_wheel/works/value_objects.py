import uuid
from dataclasses import dataclass, field
from enum import Enum

from critique_wheel.config import config


class BaseWorkDomainError(Exception):
    pass


class MissingEntryError(BaseWorkDomainError):
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


@dataclass(frozen=True)
class WorkId:
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __str__(self):
        return str(self.id)

    @property
    def hex(self):
        return self.id.hex

    def get_uuid(self):
        return str(self.id)

    @classmethod
    def from_string(cls, uuid_string: str):
        try:
            uuid_obj = uuid.UUID(uuid_string)
            return cls(id=uuid_obj)
        except ValueError:
            raise ValueError(f"Invalid UUID string: '{uuid_string}'")


@dataclass(frozen=True)
class Title:
    value: str

    def __post_init__(self):
        if len(self.value) > 100:
            raise ValueError("Title must be under 100 characters.")

    def __str__(self):
        return str(self.value)

    def __len__(self):
        return len(self.value)


@dataclass(frozen=True)
class Content:
    value: str

    def __post_init__(self):
        word_limit = config.WORK_MAX_WORDS
        if self.word_count() > word_limit:
            raise ValueError(f"Work text must be under {word_limit} words.")

    def __str__(self):
        return str(self.value)

    def __len__(self):
        return len(self.value)

    def word_count(self):
        return len(self.value.split())
