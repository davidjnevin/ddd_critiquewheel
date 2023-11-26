import pytest

import tests.end_to_end.fake_iam_repository as fake_iam_repository
import tests.end_to_end.fake_work_repository as fake_work_repository
from critique_wheel.members.models.IAM import MemberRole, MemberStatus
from critique_wheel.members.services.iam_service import IAMService
from critique_wheel.works.models.work import WorkAgeRestriction, WorkGenre, WorkStatus
from critique_wheel.works.services.work_service import WorkService


@pytest.fixture
def iam_repo():
    return fake_iam_repository.FakeMemberRepository([])


@pytest.fixture
def iam_service(iam_repo):
    return IAMService(iam_repo)


@pytest.fixture
def work_repo():
    return fake_work_repository.FakeWorkRepository([])


@pytest.fixture
def work_service(work_repo):
    return WorkService(work_repo)


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
