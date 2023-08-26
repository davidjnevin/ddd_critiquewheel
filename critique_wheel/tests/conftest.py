from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from critique_wheel.adapters.orm import mapper_registry, start_mappers
from critique_wheel.domain.models.credit import CreditManager, TransactionType
from critique_wheel.domain.models.critique import Critique
from critique_wheel.domain.models.IAM import Member, MemberRole, MemberStatus
from critique_wheel.domain.models.rating import Rating
from critique_wheel.domain.models.work import Work, WorkAgeRestriction, WorkGenre


@pytest.fixture
def valid_member():
    return Member.create(
        username="test_username",
        password="secure_unguessable_p@ssword",
        email="email_address@davidneivn.net",
        member_type=MemberRole.MEMBER,
    )
@pytest.fixture
def active_valid_member():
    return Member.create(
        username="test_username",
        password="secure_unguessable_p@ssword",
        email="email_address@davidneivn.net",
        member_type=MemberRole.MEMBER,
    )


@pytest.fixture
def valid_credit():
    return CreditManager.create(
        member_id=uuid4(),
        amount=5,
        transaction_type=TransactionType.CRITIQUE_GIVEN,
        work_id=uuid4(),
        critique_id=uuid4(),
    )

@pytest.fixture
def valid_rating():
    yield Rating.create(
        score=5,
        comment="This is a test rating.",
        member_id=uuid4(),
        critique_id=uuid4(),
    )

@pytest.fixture
def another_valid_rating():
    yield Rating.create(
        score=4,
        comment="This is a test rating.",
        member_id=uuid4(),
        critique_id=uuid4(),
    )



@pytest.fixture
def valid_critique():
    return Critique.create(
        content_about="About content.",
        content_successes="This is a test critique.",
        content_weaknesses="This is a test critique.",
        content_ideas="This is a test critique.",
        member_id=uuid4(),
        work_id=uuid4(),
        ratings=None,
    )


@pytest.fixture
def valid_work():
    return Work.create(
        title="Test Title",
        content="Test content",
        age_restriction=WorkAgeRestriction.ADULT,
        genre=WorkGenre.OTHER,
        member_id=uuid4(),
        critiques=None,
    )


@pytest.fixture
def id_critique1():
    return Critique.create(
        content_about="About content.",
        content_successes="This is a test critique.",
        content_weaknesses="This is a test critique.",
        content_ideas="This is a test critique.",
        member_id=uuid4(),
        work_id=uuid4(),
        critique_id=uuid4(),
    )


@pytest.fixture
def id_critique2():
    return Critique.create(
        content_about="About content.",
        content_successes="This is a test critique.",
        content_weaknesses="This is a test critique.",
        content_ideas="This is a test critique.",
        member_id=uuid4(),
        work_id=uuid4(),
        critique_id=uuid4(),
    )


@pytest.fixture
def valid_work_with_two_critiques():
    return Work.create(
        title="Test Title",
        content="Test content",
        age_restriction=WorkAgeRestriction.ADULT,
        genre=WorkGenre.OTHER,
        member_id=uuid4(),
        critiques=["critique1", "critique2"],
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
