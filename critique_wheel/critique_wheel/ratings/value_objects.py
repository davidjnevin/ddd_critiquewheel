import uuid
from dataclasses import dataclass, field


@dataclass(frozen=True)
class RatingId:
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __str__(self):
        return str(self.id)

    @property
    def hex(self):
        return self.id.hex

    def get_uuid(self):
        return str(self.id)


@dataclass(frozen=True)
class RatingScore:
    score: int

    def __str__(self):
        return str(self.score)

    def __int__(self):
        return self.score


@dataclass(frozen=True)
class RatingComment:
    value: str

    def __str__(self):
        return str(self.value)

    def __len__(self):
        return len(self.value)

    def word_count(self):
        return len(self.value.split())
