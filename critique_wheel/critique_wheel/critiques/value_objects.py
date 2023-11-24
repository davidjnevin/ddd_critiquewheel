import uuid
from dataclasses import dataclass, field
from enum import Enum


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
class Content:
    value: str

    def __post_init__(self):
        char_limit = 8500
        if len(self.value) > char_limit:
            raise ValueError(f"Work text must be under {char_limit} characters.")

    def __str__(self):
        return str(self.value)

    def __len__(self):
        return len(self.value)
