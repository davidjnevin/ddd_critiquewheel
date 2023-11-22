from dataclasses import dataclass, field
import uuid

@dataclass(frozen=True)
class MemberId:
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __str__(self):
        return str(self.id)


@dataclass(frozen=True)
class FirstName:
    value: str

    def __post_init__(self):
        if len(self.value) > 50:
            raise ValueError("First name must be under 50 characters.")
        if not self.value:
            raise ValueError("First name cannot be empty.")

@dataclass(frozen=True)
class LastName:
    value: str

    def __post_init__(self):
        if len(self.value) > 50:
            raise ValueError("Last name must be under 50 characters.")
        if not self.value:
            raise ValueError("Last name cannot be empty.")

@dataclass(frozen=True)
class Bio:
    value: str

    def __post_init__(self):
        word_limit = 200
        char_limit = 1200
        if len(self.value.split()) > word_limit or len(self.value) > char_limit:
            raise ValueError(f"Bio must be under {word_limit} words and {char_limit} characters.")

@dataclass(frozen=True)
class Visibility:
    value: bool

    def toggle(self):
        return Visibility(not self.value)

