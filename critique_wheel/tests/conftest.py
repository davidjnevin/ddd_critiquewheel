from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker
from sqlalchemy.pool import StaticPool

from critique_wheel.adapters.orm import mapper_registry, start_mappers
from critique_wheel.critiques.value_objects import CritiqueId
from critique_wheel.domain.models.credit import CreditManager, TransactionType
from critique_wheel.domain.models.critique import Critique
from critique_wheel.domain.models.IAM import Member, MemberRole, MemberStatus
from critique_wheel.domain.models.rating import Rating
from critique_wheel.domain.models.work import Work
from critique_wheel.infrastructure.config import config
from critique_wheel.members.value_objects import MemberId
from critique_wheel.works.value_objects import (
    Content,
    Title,
    WorkAgeRestriction,
    WorkGenre,
    WorkId,
)


@pytest.fixture
def valid_member():
    return Member.create(
        username="test_username",
        password="secure_unguessab1e_p@ssword",
        email="email_address@davidneivn.net",
        member_type=MemberRole.MEMBER,
        works=None,
        critiques=None,
    )


@pytest.fixture
def active_valid_member():
    return Member.create(
        username="active_test_username",
        password="secure_unguessab1e_p@ssword",
        email="active_email_address@davidneivn.net",
        member_type=MemberRole.MEMBER,
        status=MemberStatus.ACTIVE,
        works=None,
        critiques=None,
    )


@pytest.fixture
def valid_credit():
    return CreditManager.create(
        member_id=MemberId(),
        amount=5,
        transaction_type=TransactionType.CRITIQUE_GIVEN,
        work_id=WorkId(),
        critique_id=uuid4(),
    )


@pytest.fixture
def valid_rating():
    yield Rating.create(
        member_id=MemberId(),
        score=5,
        comment="This is a test rating.",
        critique_id=uuid4(),
    )


@pytest.fixture
def another_valid_rating():
    yield Rating.create(
        member_id=MemberId(),
        score=4,
        comment="This is a test rating.",
        critique_id=uuid4(),
    )


@pytest.fixture
def valid_critique():
    return Critique.create(
        member_id=MemberId(),
        work_id=WorkId(),
        content_about="About content.",
        content_successes="This is a test critique.",
        content_weaknesses="This is a test critique.",
        content_ideas="This is a test critique.",
        ratings=None,
    )


@pytest.fixture
def valid_work():
    return Work.create(
        title=Title("Test Title"),
        content=Content("Test content"),
        age_restriction=WorkAgeRestriction.ADULT,
        genre=WorkGenre.OTHER,
        member_id=MemberId(),
        critiques=None,
    )


@pytest.fixture
def another_valid_work():
    return Work.create(
        title=Title("Test Title 2"),
        content=Content("Test content"),
        age_restriction=WorkAgeRestriction.ADULT,
        genre=WorkGenre.FANTASY,
        member_id=MemberId(),
        critiques=None,
    )


@pytest.fixture
def id_critique1():
    return Critique.create(
        content_about="About content.",
        content_successes="This is a test critique.",
        content_weaknesses="This is a test critique.",
        content_ideas="This is a test critique.",
        member_id=MemberId(),
        work_id=WorkId(),
        critique_id=CritiqueId(),
    )


@pytest.fixture
def id_critique2():
    return Critique.create(
        content_about="About content.",
        content_successes="This is a test critique.",
        content_weaknesses="This is a test critique.",
        content_ideas="This is a test critique.",
        member_id=MemberId(),
        work_id=WorkId(),
        critique_id=CritiqueId(),
    )


@pytest.fixture
def valid_work_with_two_critiques():
    return Work.create(
        title=Title("Test Title"),
        content=Content("Test content"),
        age_restriction=WorkAgeRestriction.ADULT,
        genre=WorkGenre.OTHER,
        member_id=MemberId(),
        critiques=["critique1", "critique2"],
    )


@pytest.fixture
def in_memory_db():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        # echo=True,
    )
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    session = sessionmaker(bind=in_memory_db)()
    yield session
    clear_mappers()
    session.close()


@pytest.fixture
def postgres_db():
    engine = create_engine(config.get_postgres_uri(), echo=True)
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def postgres_session(postgres_db):
    start_mappers()
    session = sessionmaker(bind=postgres_db)()
    yield session
    clear_mappers()
    # session.close()
