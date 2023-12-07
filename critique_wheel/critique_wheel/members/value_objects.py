import uuid
from dataclasses import dataclass, field

from critique_wheel.works.exceptions.exceptions import InvalidEntryError


@dataclass(frozen=True)
class MemberId:
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
            raise InvalidEntryError(f"Invalid UUID string: '{uuid_string}'")


@dataclass(frozen=True)
class FirstName:
    value: str

    def __post_init__(self):
        if len(self.value) > 50:
            raise InvalidEntryError("First name must be under 50 characters.")
        if not self.value:
            raise InvalidEntryError("First name cannot be empty.")


@dataclass(frozen=True)
class LastName:
    value: str

    def __post_init__(self):
        if len(self.value) > 50:
            raise InvalidEntryError("Last name must be under 50 characters.")
        if not self.value:
            raise InvalidEntryError("Last name cannot be empty.")


@dataclass(frozen=True)
class Bio:
    value: str

    def __post_init__(self):
        word_limit = 200
        char_limit = 1200
        if len(self.value.split()) > word_limit or len(self.value) > char_limit:
            raise InvalidEntryError(
                f"Bio must be under {word_limit} words and {char_limit} characters."
            )


@dataclass(frozen=True)
class Visibility:
    value: bool

    def toggle(self):
        return Visibility(not self.value)
