import logging
import uuid
from dataclasses import dataclass, field
from enum import Enum

from critique_wheel.config import config
from critique_wheel.works.exceptions import exceptions

logger = logging.getLogger(__name__)


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


def find_agerestriction_by_value(value: str) -> WorkAgeRestriction:
    for genre in WorkAgeRestriction:
        if genre.value == value:
            return genre
    raise ValueError(f"{value} is not a valid WorkAgeRestriction")


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


def find_genre_by_value(value: str) -> WorkGenre:
    for genre in WorkGenre:
        if genre.value == value:
            return genre
    raise ValueError(f"{value} is not a valid WorkGenre")


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
        if not uuid_string:
            return None
        try:
            uuid_obj = uuid.UUID(uuid_string)
            return cls(id=uuid_obj)
        except ValueError:
            logger.exception(f"Invalid UUID string: '{uuid_string}'")
            raise exceptions.InvalidEntryError(f"Invalid UUID string: '{uuid_string}'")


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
            raise exceptions.InvalidEntryError(
                f"Work text must be under {word_limit} words."
            )

    def __str__(self):
        return str(self.value)

    def __len__(self):
        return len(self.value)

    def word_count(self):
        return len(self.value.split())
