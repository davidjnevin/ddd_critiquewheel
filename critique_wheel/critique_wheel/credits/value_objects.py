import uuid
from dataclasses import dataclass, field


class BaseCreditDomainError(Exception):
    pass


class MissingEntryError(BaseCreditDomainError):
    pass


@dataclass(frozen=True)
class TransactionId:
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __str__(self):
        return str(self.id)

    @property
    def hex(self):
        return self.id.hex

    def get_uuid(self):
        return str(self.id)
