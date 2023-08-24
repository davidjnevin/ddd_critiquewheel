import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from uuid import uuid4
from critique_wheel.domain.models.work import Work, WorkAgeRestriction, WorkGenre
from critique_wheel.domain.models.critique import Critique, CritiqueStatus
from critique_wheel.adapters.orm import mapper_registry, start_mappers


@pytest.fixture
def valid_critique():
    return Critique.create(
        content_about="About content.",
        content_successes="This is a test critique.",
        content_weaknesses="This is a test critique.",
        content_ideas="This is a test critique.",
        member_id=uuid4(),
        work_id=uuid4(),
    )
@pytest.fixture
def valid_work():
    return Work.create(
        title="Test Title",
        content="Test content",
        age_restriction=WorkAgeRestriction.ADULT,
        genre=WorkGenre.OTHER,
        member_id=uuid4(),
    )

@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()
