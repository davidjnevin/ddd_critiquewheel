from datetime import datetime
from sqlalchemy import Uuid

from sqlalchemy import Column, DateTime, Enum, Integer, String, Table, MetaData
from sqlalchemy.orm import registry

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
    Column("member_id", Uuid(as_uuid=True))
)


def start_mappers():
    mapper_registry.map_imperatively(Work, works_table)
