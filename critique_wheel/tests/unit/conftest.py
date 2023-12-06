import pytest

import tests.e2e.fake_iam_repository as fake_iam_repository
from critique_wheel.members.services.iam_service import IAMService


@pytest.fixture
def iam_repo():
    return fake_iam_repository.FakeMemberRepository([])


@pytest.fixture
def iam_service(iam_repo):
    return IAMService(iam_repo)


# @pytest.fixture
# def work_repo():
#     return fake_work_repository.FakeWorkRepository([])


# @pytest.fixture
# def work_service(work_repo):
#     return WorkService(work_repo)
