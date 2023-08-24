from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Integer, String, Table, Uuid
from sqlalchemy.orm import registry

from critique_wheel.domain.models.critique import Critique, CritiqueStatus
from critique_wheel.domain.models.rating import Rating, RatingStatus
from critique_wheel.domain.models.work import (
    Work,
    WorkAgeRestriction,
    WorkGenre,
    WorkStatus,
)

mapper_registry = registry()

works_table = Table(
    "works",
    mapper_registry.metadata,
    Column("id", Uuid(as_uuid=True), primary_key=True),
    Column("title", String),
    Column("content", String),
    Column("age_restriction", Enum(WorkAgeRestriction)),
    Column("genre", Enum(WorkGenre)),
    Column("status", Enum(WorkStatus)),
    Column("word_count", Integer),
    Column("submission_date", DateTime, default=datetime.now),
    Column("last_update_date", DateTime, default=datetime.now),
    Column("archive_date", DateTime),
    Column("member_id", Uuid(as_uuid=True)),
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
    Column("member_id", Uuid(as_uuid=True)),
    Column("work_id", Uuid(as_uuid=True)),
)

ratings_table = Table(
    "ratings",
    mapper_registry.metadata,
    Column("id", Uuid(as_uuid=True), primary_key=True),
    Column("score", Integer),
    Column("comment", String),
    Column("status", Enum(RatingStatus)),
    Column("submission_date", DateTime, default=datetime.now),
    Column("last_update_date", DateTime, default=datetime.now),
    Column("archive_date", DateTime),
    Column("member_id", Uuid(as_uuid=True)),
    Column("critique_id", Uuid(as_uuid=True)),
)


def start_mappers():
    mapper_registry.map_imperatively(Work, works_table)
    mapper_registry.map_imperatively(Critique, critique_table)
    # In order to maintain the invariant that a Rating is always associated with a Critique and a Member,
    # we need to map the Rating class imperatively, and then add the Critique and Member as properties.
    mapper_registry.map_imperatively(
        Rating,
        ratings_table,
        properties={
            "_critique_id": ratings_table.c.critique_id,
            "_member_id": ratings_table.c.member_id
        }
    )
