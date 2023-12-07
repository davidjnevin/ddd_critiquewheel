import pytest

import tests.integration.fake_iam_repository as fake_iam_repository
from critique_wheel.members.services.iam_service import IAMService


@pytest.fixture
def iam_repo():
    return fake_iam_repository.FakeMemberRepository([])


@pytest.fixture
def iam_service(iam_repo):
    return IAMService(iam_repo)
