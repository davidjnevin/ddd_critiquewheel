from uuid import uuid4

import pytest

from critique_wheel.members.value_objects import MemberId
from critique_wheel.works.services import work_service
from tests.integration.fake_work_repository import FakeWorkRepository


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


def test_add_work(work_details):
    member_id = str(uuid4())
    repo = FakeWorkRepository([])
    session = FakeSession()
    work = work_service.add_work(
        work_id=None,
        title=work_details["title"],
        content=work_details["content"],
        age_restriction=work_details["age_restriction"],
        genre=work_details["genre"],
        member_id=member_id,
        repo=repo,
        session=session,
    )
    assert str(work.title) == "Test Title"
    assert str(work.content) == "Test content"
    assert work.member_id is not None
    assert work.genre == "YOUNG ADULT"
    assert work.status == "PENDING REVIEW"
    assert work.age_restriction == "ADULT"
    assert work.critiques == []
    assert session.committed is True


def test_get_work_by_id(work_details):
    repo = FakeWorkRepository([])
    session = FakeSession()
    work_id = str(uuid4())
    member_id = str(uuid4())
    work = work_service.add_work(
        work_id=work_id,
        title=work_details["title"],
        content=work_details["content"],
        age_restriction=work_details["age_restriction"],
        genre=work_details["genre"],
        member_id=member_id,
        repo=repo,
        session=session,
    )
    retrieved_work = work_service.get_work_by_id(work_id=work_id, repo=repo)
    assert retrieved_work == work


def test_create_dupliacte_work_raises_DuplicateWorkError(work_details):
    member_id = MemberId()
    repo = FakeWorkRepository([])
    session = FakeSession()
    work_id = str(uuid4())
    member_id = str(uuid4())
    work_service.add_work(
        work_id=work_id,
        title=work_details["title"],
        content=work_details["content"],
        age_restriction=work_details["age_restriction"],
        genre=work_details["genre"],
        member_id=member_id,
        repo=repo,
        session=session,
    )
    with pytest.raises(work_service.DuplicateWorkError):
        work_service.add_work(
            work_id=work_id,
            title=work_details["title"],
            content=work_details["content"],
            age_restriction=work_details["age_restriction"],
            genre=work_details["genre"],
            member_id=member_id,
            repo=repo,
            session=session,
        )


def test_add_work_raises_InvalidDataError_when_title_is_empty(work_details):
    member_id = MemberId()
    repo = FakeWorkRepository([])
    session = FakeSession()
    work_id = str(uuid4())
    member_id = str(uuid4())
    with pytest.raises(work_service.InvalidDataError):
        work_service.add_work(
            work_id=work_id,
            title="",
            content=work_details["content"],
            age_restriction=work_details["age_restriction"],
            genre=work_details["genre"],
            member_id=member_id,
            repo=repo,
            session=session,
        )


def test_add_work_raises_InvalidDataError_when_age_restriction_is_empty(work_details):
    member_id = MemberId()
    repo = FakeWorkRepository([])
    session = FakeSession()
    work_id = str(uuid4())
    member_id = str(uuid4())
    with pytest.raises(work_service.InvalidDataError):
        work_service.add_work(
            work_id=work_id,
            title=work_details["title"],
            content=work_details["content"],
            age_restriction="",
            genre=work_details["genre"],
            member_id=member_id,
            repo=repo,
            session=session,
        )


def test_add_work_raises_InvalidDataError_when_genre_is_empty(work_details):
    member_id = MemberId()
    repo = FakeWorkRepository([])
    session = FakeSession()
    work_id = str(uuid4())
    member_id = str(uuid4())
    with pytest.raises(work_service.InvalidDataError):
        work_service.add_work(
            work_id=work_id,
            title=work_details["title"],
            content=work_details["content"],
            age_restriction=work_details["age_restriction"],
            genre="",
            member_id=member_id,
            repo=repo,
            session=session,
        )


def test_add_work_raises_InvalidDataError_when_content_is_empty(work_details):
    member_id = MemberId()
    repo = FakeWorkRepository([])
    session = FakeSession()
    work_id = str(uuid4())
    member_id = str(uuid4())
    with pytest.raises(work_service.InvalidDataError):
        work_service.add_work(
            work_id=work_id,
            title=work_details["title"],
            content="",
            age_restriction=work_details["age_restriction"],
            genre=work_details["genre"],
            member_id=member_id,
            repo=repo,
            session=session,
        )


def test_add_work_raises_member_exception_InvalidDataError_when_member_id_is_None(
    work_details
):
    repo = FakeWorkRepository([])
    session = FakeSession()
    work_id = str(uuid4())
    with pytest.raises(work_service.InvalidDataError):
        work_service.add_work(
            work_id=work_id,
            title=work_details["title"],
            content=work_details["content"],
            age_restriction=work_details["age_restriction"],
            genre=work_details["genre"],
            member_id="",
            repo=repo,
            session=session,
        )


def test_list_works(work_details):
    repo = FakeWorkRepository([])
    session = FakeSession()
    work_id = str(uuid4())
    member_id = str(uuid4())
    work_id_2 = str(uuid4())
    member_id_2 = str(uuid4())
    work_1 = work_service.add_work(
        work_id=work_id,
        title=work_details["title"],
        content=work_details["content"],
        age_restriction=work_details["age_restriction"],
        genre=work_details["genre"],
        member_id=member_id,
        repo=repo,
        session=session,
    )
    work_2 = work_service.add_work(
        work_id=work_id_2,
        title=work_details["title"],
        content=work_details["content"],
        age_restriction=work_details["age_restriction"],
        genre=work_details["genre"],
        member_id=member_id_2,
        repo=repo,
        session=session,
    )
    works = work_service.list_works(repo)
    assert len(works) == 2
    assert work_1 in works
    assert work_2 in works


def test_list_works_returns_empty_list_when_no_works_exist():
    repo = FakeWorkRepository([])
    works = work_service.list_works(repo)
    assert len(works) == 0
    assert works == []
