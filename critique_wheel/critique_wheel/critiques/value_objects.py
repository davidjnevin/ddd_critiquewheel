import uuid
from dataclasses import dataclass, field
from enum import Enum

from critique_wheel.config import config


class BaseCritiqueDomainError(Exception):
    pass


class MissingEntryError(BaseCritiqueDomainError):
    pass


class CritiqueStatus(str, Enum):
    PENDING_REVIEW = "PENDING REVIEW"
    ACTIVE = "ACTIVE"
    REJECTED = "REJECTED"
    ARCHIVED = "ARCHIVED"
    MARKED_FOR_DELETION = "MARKED FOR DELETION"


@dataclass(frozen=True)
class CritiqueId:
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __str__(self):
        return str(self.id)

    @property
    def hex(self):
        return self.id.hex

    def get_uuid(self):
        return str(self.id)


@dataclass(frozen=True)
class CritiqueAbout:
    value: str
    minimum_words = config.CRITIQUE_ABOUT_MIN_WORDS

    def is_minimum_word_length(self):
        return satisfies_minimum_word_count(self.value, self.minimum_words)

    def __str__(self):
        return str(self.value)

    def __len__(self):
        return len(self.value)

    def word_count(self):
        return len(self.value.split())


@dataclass(frozen=True)
class CritiqueSuccesses:
    value: str
    minimum_words = config.CRITIQUE_SUCCESSES_MIN_WORDS

    def is_minimum_word_length(self):
        return satisfies_minimum_word_count(self.value, self.minimum_words)

    def __str__(self):
        return str(self.value)

    def __len__(self):
        return len(self.value)

    def word_count(self):
        return len(self.value.split())


@dataclass(frozen=True)
class CritiqueWeaknesses:
    value: str
    minimum_words = config.CRITIQUE_WEAKNESSES_MIN_WORDS

    def is_minimum_word_length(self):
        return satisfies_minimum_word_count(self.value, self.minimum_words)

    def __str__(self):
        return str(self.value)

    def __len__(self):
        return len(self.value)

    def word_count(self):
        return len(self.value.split())


@dataclass(frozen=True)
class CritiqueIdeas:
    value: str
    minimum_words = config.CRITIQUE_IDEAS_MIN_WORDS

    def is_minimum_word_length(self):
        return satisfies_minimum_word_count(self.value, self.minimum_words)

    def __str__(self):
        return str(self.value)

    def __len__(self):
        return len(self.value)

    def word_count(self):
        return len(self.value.split())


def satisfies_minimum_word_count(value, minimum_words):
    return len(value.split()) <= minimum_words
