import uuid

from sqlalchemy import Integer, String
from sqlalchemy.types import CHAR, TypeDecorator

from critique_wheel.credits.value_objects import TransactionId
from critique_wheel.critiques.value_objects import (
    CritiqueAbout,
    CritiqueId,
    CritiqueIdeas,
    CritiqueSuccesses,
    CritiqueWeaknesses,
)
from critique_wheel.members.value_objects import MemberId
from critique_wheel.ratings.value_objects import RatingComment, RatingId, RatingScore
from critique_wheel.works.value_objects import Content, Title, WorkId


class WorkUUIDType(TypeDecorator):
    impl = CHAR(36)
    cache_ok = True  # Indicate that this type is safe to cache

    def process_bind_param(self, value, dialect):
        return str(value) if value is not None else None

    def process_result_value(self, value, dialect):
        return WorkId(id=uuid.UUID(value)) if value is not None else None


class TitleType(TypeDecorator):
    impl = String
    cache_ok = True  # Indicate that this type is safe to cache

    def process_bind_param(self, value, dialect):
        return value.value if value is not None else None

    def process_result_value(self, value, dialect):
        return Title(value) if value is not None else None


class ContentType(TypeDecorator):
    impl = String
    cache_ok = True  # Indicate that this type is safe to cache

    def process_bind_param(self, value, dialect):
        return value.value if value is not None else None

    def process_result_value(self, value, dialect):
        return Content(value) if value is not None else None


class MemberUUIDType(TypeDecorator):
    impl = CHAR(36)
    cache_ok = True  # Indicate that this type is safe to cache

    def process_bind_param(self, value, dialect):
        return str(value) if value is not None else None

    def process_result_value(self, value, dialect):
        return MemberId(id=uuid.UUID(value)) if value is not None else None


class CritiqueUUIDType(TypeDecorator):
    impl = CHAR(36)
    cache_ok = True  # Indicate that this type is safe to cache

    def process_bind_param(self, value, dialect):
        return str(value) if value is not None else None

    def process_result_value(self, value, dialect):
        return CritiqueId(id=uuid.UUID(value)) if value is not None else None


class CritiqueAboutType(TypeDecorator):
    impl = String
    cache_ok = True  # Indicate that this type is safe to cache

    def process_bind_param(self, value, dialect):
        return value.value if value is not None else None

    def process_result_value(self, value, dialect):
        return CritiqueAbout(value) if value is not None else None


class CritiqueSuccesesType(TypeDecorator):
    impl = String
    cache_ok = True  # Indicate that this type is safe to cache

    def process_bind_param(self, value, dialect):
        return value.value if value is not None else None

    def process_result_value(self, value, dialect):
        return CritiqueSuccesses(value) if value is not None else None


class CritiqueWeaknessesType(TypeDecorator):
    impl = String
    cache_ok = True  # Indicate that this type is safe to cache

    def process_bind_param(self, value, dialect):
        return value.value if value is not None else None

    def process_result_value(self, value, dialect):
        return CritiqueWeaknesses(value) if value is not None else None


class CritiqueIdeasType(TypeDecorator):
    impl = String
    cache_ok = True  # Indicate that this type is safe to cache

    def process_bind_param(self, value, dialect):
        return value.value if value is not None else None

    def process_result_value(self, value, dialect):
        return CritiqueIdeas(value) if value is not None else None


class RatingUUIDType(TypeDecorator):
    impl = CHAR(36)
    cache_ok = True  # Indicate that this type is safe to cache

    def process_bind_param(self, value, dialect):
        return str(value) if value is not None else None

    def process_result_value(self, value, dialect):
        return RatingId(id=uuid.UUID(value)) if value is not None else None


class RatingScoreType(TypeDecorator):
    impl = Integer
    cache_ok = False  # Indicate that this type is safe to cache

    def process_bind_param(self, value, dialect):
        return int(value) if value is not None else None

    def process_result_value(self, value, dialect):
        return RatingScore(value) if value is not None else None


class RatingCommentStringType(TypeDecorator):
    impl = String
    cache_ok = True  # Indicate that this type is safe to cache

    def process_bind_param(self, value, dialect):
        return value.value if value is not None else None

    def process_result_value(self, value, dialect):
        return RatingComment(value) if value is not None else None


class TransactionUUIDType(TypeDecorator):
    impl = CHAR(36)
    cache_ok = True  # Indicate that this type is safe to cache

    def process_bind_param(self, value, dialect):
        return str(value) if value is not None else None

    def process_result_value(self, value, dialect):
        return TransactionId(id=uuid.UUID(value)) if value is not None else None
