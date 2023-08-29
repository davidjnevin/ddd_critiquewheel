from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, MetaData, String, Table, Uuid
from sqlalchemy.orm import registry, relationship

from critique_wheel.domain.models.credit import CreditManager, TransactionType
from critique_wheel.domain.models.critique import Critique, CritiqueStatus
from critique_wheel.domain.models.IAM import Member, MemberRole, MemberStatus
from critique_wheel.domain.models.rating import Rating, RatingStatus
from critique_wheel.domain.models.work import (
    Work,
    WorkAgeRestriction,
    WorkGenre,
    WorkStatus,
)
mapper_registry = registry()

work_table = Table(
    "works",
    mapper_registry.metadata,
    Column("id", Uuid(as_uuid=True), primary_key=True, nullable=False),
    Column("title", String),
    Column("content", String),
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
    Column("id", Uuid(as_uuid=True), primary_key=True),
    Column("content_about", String),
    Column("content_successes", String),
    Column("content_weaknesses", String),
    Column("content_ideas", String),
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
    Column("id", Uuid(as_uuid=True), primary_key=True),
    Column("score", Integer),
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
    Column("id", Uuid(as_uuid=True), primary_key=True),
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
    Column("id", Uuid(as_uuid=True), primary_key=True),
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
        properties={"ratings": relationship(Rating, backref="critiques", order_by=rating_table.c.id)},
    )
    # WORK
    mapper_registry.map_imperatively(
        Work,
        work_table,
        properties={
            "critiques": relationship(Critique, backref="work", order_by=critique_table.c.id),
        },
    )
    # MEMBER
    mapper_registry.map_imperatively(
        Member,
        member_table,
        properties={
            "works": relationship(Work, backref="members", order_by=work_table.c.id),
            "critiques": relationship(Critique, backref="members", order_by=critique_table.c.id),
            "ratings": relationship(Rating, backref="members", order_by=rating_table.c.id),
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
