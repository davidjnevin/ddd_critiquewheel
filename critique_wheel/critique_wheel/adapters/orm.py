import logging
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Table
from sqlalchemy.orm import registry, relationship

from critique_wheel.adapters.orm_domain_types import (
    ContentType,
    CritiqueAboutType,
    CritiqueIdeasType,
    CritiqueSuccesesType,
    CritiqueUUIDType,
    CritiqueWeaknessesType,
    MemberUUIDType,
    RatingCommentStringType,
    RatingScoreType,
    RatingUUIDType,
    TitleType,
    TransactionUUIDType,
    WorkUUIDType,
)
from critique_wheel.credits.models.credit import CreditManager, TransactionType
from critique_wheel.critiques.models.critique import Critique, CritiqueStatus
from critique_wheel.members.models.IAM import Member, MemberRole, MemberStatus
from critique_wheel.ratings.models.rating import Rating, RatingStatus
from critique_wheel.works.models.work import (
    Work,
    WorkAgeRestriction,
    WorkGenre,
    WorkStatus,
)

logger = logging.getLogger(__name__)
mapper_registry = registry()


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
    Column("comment", RatingCommentStringType),
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
    Column("username", String(255)),
    Column("email", String(255)),
    Column("password", String(255)),
    Column("member_type", Enum(MemberRole)),
    Column("status", Enum(MemberStatus)),
    Column("last_login", DateTime, default=datetime.now),
    Column("last_update_date", DateTime, default=datetime.now),
    Column("created_date", DateTime, default=datetime.now),
    Column("archive_date", DateTime),
)


def start_mappers():
    logger.debug("Starting orm mappers")
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
                Critique, backref="works", order_by=critique_table.c.id
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
