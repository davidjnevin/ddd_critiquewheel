import logging
import os
import time

import pytest
import requests
from requests.exceptions import ConnectionError
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import clear_mappers, sessionmaker

from critique_wheel.adapters.orm import mapper_registry, start_mappers
from critique_wheel.credits.models.credit import CreditManager, TransactionType
from critique_wheel.critiques.models.critique import Critique
from critique_wheel.critiques.value_objects import (
    CritiqueAbout,
    CritiqueId,
    CritiqueIdeas,
    CritiqueSuccesses,
    CritiqueWeaknesses,
)
from critique_wheel.members.models.IAM import Member, MemberRole, MemberStatus
from critique_wheel.members.value_objects import MemberId
from critique_wheel.ratings.models.rating import Rating
from critique_wheel.works.models.work import Work
from critique_wheel.works.value_objects import (
    Content,
    Title,
    WorkAgeRestriction,
    WorkGenre,
    WorkId,
    WorkStatus,
)

os.environ["ENV_STATE"] = "test"
from critique_wheel import config  # noqa : E402

logger = logging.getLogger(__name__)


@pytest.fixture
def in_memory_sqlite_db():
    engine = create_engine("sqlite:///:memory:")
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def sqlite_session_factory(in_memory_sqlite_db):
    yield sessionmaker(bind=in_memory_sqlite_db)


@pytest.fixture
def mappers():
    start_mappers()
    yield
    clear_mappers()


@pytest.fixture
def session(sqlite_session_factory):
    return sqlite_session_factory()


def wait_for_postgres_to_come_up(engine):
    deadline = time.time() + 1
    while time.time() < deadline:
        try:
            return engine.connect()
        except OperationalError:
            logger.exception("Postgres not up yet")
            time.sleep(0.5)
    pytest.fail("Postgres never came up")


def wait_for_webapp_to_come_up():
    deadline = time.time() + 5
    url = config.get_api_url()
    logger.debug(f"Waiting for {url} to come up")
    while time.time() < deadline:
        try:
            return requests.get(url)
        except ConnectionError:
            logger.exception("Webapp not up yet")
            time.sleep(0.5)
    pytest.fail("API never came up")


@pytest.fixture(scope="session")
def postgres_db():
    engine = create_engine(config.get_postgres_uri())  # echo=True option
    wait_for_postgres_to_come_up(engine)
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def postgres_session(postgres_db):
    yield sessionmaker(bind=postgres_db)()


@pytest.fixture
def valid_member():
    yield Member.create(
        username="test_username",
        password="secure_unguessab1e_p@ssword",
        email="email_address@davidneivn.net",
        member_type=MemberRole.MEMBER,
        works=None,
        critiques=None,
    )


@pytest.fixture
def active_valid_member():
    yield Member.create(
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
        critique_id=CritiqueId(),
    )


@pytest.fixture
def valid_rating():
    yield Rating.create(
        member_id=MemberId(),
        score=5,
        comment="This is a test rating.",
        critique_id=CritiqueId(),
    )


@pytest.fixture
def another_valid_rating():
    yield Rating.create(
        member_id=MemberId(),
        score=4,
        comment="This is a test rating.",
        critique_id=CritiqueId(),
    )


@pytest.fixture
def valid_critique():
    text = "Word " * 45
    yield Critique.create(
        critique_about=CritiqueAbout(text),
        critique_successes=CritiqueSuccesses(text),
        critique_weaknesses=CritiqueWeaknesses(text),
        critique_ideas=CritiqueIdeas(text),
        member_id=MemberId(),
        work_id=WorkId(),
        critique_id=CritiqueId(),
        ratings=None,
    )


@pytest.fixture
def valid_work():
    yield Work.create(
        title=Title("Test Title"),
        content=Content("Test content"),
        age_restriction=WorkAgeRestriction.ADULT,
        genre=WorkGenre.OTHER,
        member_id=MemberId(),
        critiques=None,
    )


@pytest.fixture
def another_valid_work():
    yield Work.create(
        title=Title("Test Title 2"),
        content=Content("Test content"),
        age_restriction=WorkAgeRestriction.ADULT,
        genre=WorkGenre.FANTASY,
        member_id=MemberId(),
        critiques=None,
    )


@pytest.fixture
def valid_critique1():
    text = "Word " * 45
    yield Critique.create(
        critique_about=CritiqueAbout(text),
        critique_successes=CritiqueSuccesses(text),
        critique_weaknesses=CritiqueWeaknesses(text),
        critique_ideas=CritiqueIdeas(text),
        member_id=MemberId(),
        work_id=WorkId(),
        critique_id=CritiqueId(),
    )


@pytest.fixture
def valid_critique2():
    text = "Word " * 45
    yield Critique.create(
        critique_about=CritiqueAbout(text),
        critique_successes=CritiqueSuccesses(text),
        critique_weaknesses=CritiqueWeaknesses(text),
        critique_ideas=CritiqueIdeas(text),
        member_id=MemberId(),
        work_id=WorkId(),
        critique_id=CritiqueId(),
    )


@pytest.fixture
def valid_work_with_two_critiques(valid_critique1, valid_critique2):
    work = Work.create(
        title=Title("Test Title"),
        content=Content("Test content"),
        age_restriction=WorkAgeRestriction.ADULT,
        genre=WorkGenre.OTHER,
        member_id=MemberId(),
        critiques=[],
    )
    work.status = WorkStatus.ACTIVE
    valid_critique1.work_id = work.id
    valid_critique2.work_id = work.id
    work.add_critique(valid_critique1)
    work.add_critique(valid_critique2)
    return work


@pytest.fixture
def member_details():
    return {
        "username": "test_username",
        "email": "testing_email@davidnevin.net",
        "password": "secure_unguessable_p@ssword",
        "member_type": MemberRole.MEMBER,
        "status": MemberStatus.INACTIVE,
    }


@pytest.fixture
def work_details():
    return {
        "title": "Test Title",
        "content": "Test content",
        "status": WorkStatus.PENDING_REVIEW,
        "age_restriction": WorkAgeRestriction.ADULT,
        "genre": WorkGenre.YOUNGADULT,
    }
