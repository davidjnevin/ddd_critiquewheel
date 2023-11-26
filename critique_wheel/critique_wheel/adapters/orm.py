import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Table
from sqlalchemy.orm import registry, relationship
from sqlalchemy.types import CHAR, TypeDecorator

from critique_wheel.credits.value_objects import TransactionId
from critique_wheel.critiques.value_objects import (
    CritiqueAbout,
    CritiqueId,
    CritiqueIdeas,
    CritiqueSuccesses,
    CritiqueWeaknesses,
)
from critique_wheel.domain.models.credit import CreditManager, TransactionType
from critique_wheel.domain.models.critique import Critique, CritiqueStatus
from critique_wheel.domain.models.IAM import Member, MemberRole, MemberStatus
from critique_wheel.domain.models.rating import Rating, RatingStatus
from critique_wheel.domain.models.work import Work
from critique_wheel.members.value_objects import MemberId
from critique_wheel.ratings.value_objects import RatingComment, RatingId, RatingScore
from critique_wheel.works.value_objects import (
    Content,
    Title,
    WorkAgeRestriction,
    WorkGenre,
    WorkId,
    WorkStatus,
)

mapper_registry = registry()


class WorkUUIDType(TypeDecorator):
    impl = CHAR
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
    impl = CHAR
    cache_ok = True  # Indicate that this type is safe to cache

    def process_bind_param(self, value, dialect):
        return str(value) if value is not None else None

    def process_result_value(self, value, dialect):
        return MemberId(id=uuid.UUID(value)) if value is not None else None


class CritiqueUUIDType(TypeDecorator):
    impl = CHAR
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
    impl = CHAR
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
    impl = CHAR
    cache_ok = True  # Indicate that this type is safe to cache

    def process_bind_param(self, value, dialect):
        return str(value) if value is not None else None

    def process_result_value(self, value, dialect):
        return TransactionId(id=uuid.UUID(value)) if value is not None else None


work_table = Table(
    "works",
    mapper_registry.metadata,
    Column("id", WorkUUIDType, primary_key=True, nullable=False),
    Column("title", TitleType),
    Column("content", ContentType),
    Column("age_restriction", Enum(WorkAgeRestriction)),
    Column("genre", Enum(WorkGenre)),
    Column("status", Enum(WorkStatus)),
    Column("word_count", Integer),
    Column("submission_date", DateTime, default=datetime.now),
    Column("last_update_date", DateTime, default=datetime.now),
    Column("archive_date", DateTime),
    Column("member_id", ForeignKey("members.id")),
)


critique_table = Table(
    "critiques",
    mapper_registry.metadata,
    Column("id", CritiqueUUIDType, primary_key=True, nullable=False),
    Column("critique_about", CritiqueAboutType),
    Column("critique_successes", CritiqueSuccesesType),
    Column("critique_weaknesses", CritiqueWeaknessesType),
    Column("critique_ideas", CritiqueIdeasType),
    Column("status", Enum(CritiqueStatus)),
    Column("submission_date", DateTime, default=datetime.now),
    Column("last_update_date", DateTime, default=datetime.now),
    Column("archive_date", DateTime),
    Column("member_id", ForeignKey("members.id")),
    Column("work_id", ForeignKey("works.id")),
)

rating_table = Table(
    "ratings",
    mapper_registry.metadata,
    Column("id", RatingUUIDType, primary_key=True),
    Column("score", RatingScoreType),
    Column("comment", String),
    Column("status", Enum(RatingStatus)),
    Column("member_id", ForeignKey("members.id"), nullable=False),
    Column("critique_id", ForeignKey("critiques.id"), nullable=False),
    Column("submission_date", DateTime, default=datetime.now),
    Column("last_update_date", DateTime, default=datetime.now),
    Column("archive_date", DateTime),
)

credit_table = Table(
    "credits",
    mapper_registry.metadata,
    Column("id", TransactionUUIDType, primary_key=True),
    Column("member_id", ForeignKey("members.id")),
    Column("critique_id", ForeignKey("critiques.id")),
    Column("work_id", ForeignKey("works.id")),
    Column("amount", Integer),
    Column("date_of_transaction", DateTime, default=datetime.now),
    Column("transaction_type", Enum(TransactionType)),
)

member_table = Table(
    "members",
    mapper_registry.metadata,
    Column("id", MemberUUIDType, primary_key=True),
    Column("username", String),
    Column("email", String),
    Column("password", String),
    Column("member_type", Enum(MemberRole)),
    Column("status", Enum(MemberStatus)),
    Column("last_login", DateTime, default=datetime.now),
    Column("last_update_date", DateTime, default=datetime.now),
    Column("crated_date", DateTime, default=datetime.now),
    Column("archive_date", DateTime),
)


def start_mappers():
    # CRITIQUE
    mapper_registry.map_imperatively(
        Critique,
        critique_table,
        properties={
            "ratings": relationship(
                Rating, backref="critiques", order_by=rating_table.c.id
            )
        },
    )
    # WORK
    mapper_registry.map_imperatively(
        Work,
        work_table,
        properties={
            "critiques": relationship(
                Critique, backref="work", order_by=critique_table.c.id
            ),
        },
    )
    # MEMBER
    mapper_registry.map_imperatively(
        Member,
        member_table,
        properties={
            "works": relationship(Work, backref="members", order_by=work_table.c.id),
            "critiques": relationship(
                Critique, backref="members", order_by=critique_table.c.id
            ),
            "ratings": relationship(
                Rating, backref="members", order_by=rating_table.c.id
            ),
        },
    )

    # RATING
    # In order to maintain the invariant that a Rating is always associated with a Critique and a Member,
    # we need to map the Rating class imperatively, and then add the Critique and Member as properties.
    mapper_registry.map_imperatively(
        Rating,
        rating_table,
        properties={
            "_critique_id": rating_table.c.critique_id,
            "_member_id": rating_table.c.member_id,
        },
    )
    # CREDIT
    mapper_registry.map_imperatively(CreditManager, credit_table)
