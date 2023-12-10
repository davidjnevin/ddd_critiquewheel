from uuid import uuid4

import pytest

from critique_wheel.members.value_objects import MemberId
from critique_wheel.works.services import unit_of_work, work_service
from tests.integration import fake_work_repository


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.works = fake_work_repository.FakeWorkRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_add_work(work_details):
    member_id = str(uuid4())
    work_id = str(uuid4())
    uow = FakeUnitOfWork()
    work = work_service.add_work(
        uow=uow,
        work_id=work_id,
        title=work_details["title"],
        content=work_details["content"],
        age_restriction=work_details["age_restriction"],
        genre=work_details["genre"],
        member_id=member_id,
    )
    assert uow.committed
    assert work["title"] == "Test Title"
    assert work["content"] == "Test content"
    assert work["member_id"] is not None
    assert work["genre"] == "YOUNG ADULT"
    assert work["status"] == "PENDING REVIEW"
    assert work["age_restriction"] == "ADULT"
    assert work["critiques"] == []


def test_get_work_by_id(work_details):
    member_id = str(uuid4())
    work_id = str(uuid4())
    uow = FakeUnitOfWork()
    work = work_service.add_work(
        uow=uow,
        work_id=work_id,
        title=work_details["title"],
        content=work_details["content"],
        age_restriction=work_details["age_restriction"],
        genre=work_details["genre"],
        member_id=member_id,
    )
    retrieved_work = work_service.get_work_by_id(work_id=work["id"], uow=uow)

    assert uow.committed
    assert retrieved_work == work


def test_create_dupliacte_work_raises_DuplicateWorkError(work_details):
    member_id = str(uuid4())
    work_id = str(uuid4())
    member_id = str(uuid4())
    uow = FakeUnitOfWork()
    work_service.add_work(
        uow=uow,
        work_id=work_id,
        title=work_details["title"],
        content=work_details["content"],
        age_restriction=work_details["age_restriction"],
        genre=work_details["genre"],
        member_id=member_id,
    )
    with pytest.raises(work_service.DuplicateWorkError):
        work_service.add_work(
            uow=uow,
            work_id=work_id,
            title=work_details["title"],
            content=work_details["content"],
            age_restriction=work_details["age_restriction"],
            genre=work_details["genre"],
            member_id=member_id,
        )


def test_add_work_raises_InvalidDataError_when_title_is_empty(work_details):
    member_id = MemberId()
    work_id = str(uuid4())
    member_id = str(uuid4())
    uow = FakeUnitOfWork()
    with pytest.raises(work_service.InvalidDataError):
        work_service.add_work(
            uow=uow,
            work_id=work_id,
            title="",
            content=work_details["content"],
            age_restriction=work_details["age_restriction"],
            genre=work_details["genre"],
            member_id=member_id,
        )


def test_add_work_raises_InvalidDataError_when_age_restriction_is_empty(work_details):
    member_id = MemberId()
    work_id = str(uuid4())
    member_id = str(uuid4())
    uow = FakeUnitOfWork()
    with pytest.raises(work_service.InvalidDataError):
        work_service.add_work(
            uow=uow,
            work_id=work_id,
            title=work_details["title"],
            content=work_details["content"],
            age_restriction="",
            genre=work_details["genre"],
            member_id=member_id,
        )


def test_add_work_raises_InvalidDataError_when_genre_is_empty(work_details):
    member_id = MemberId()
    work_id = str(uuid4())
    member_id = str(uuid4())
    uow = FakeUnitOfWork()
    with pytest.raises(work_service.InvalidDataError):
        work_service.add_work(
            uow=uow,
            work_id=work_id,
            title=work_details["title"],
            content=work_details["content"],
            age_restriction=work_details["age_restriction"],
            genre="",
            member_id=member_id,
        )


def test_add_work_raises_InvalidDataError_when_content_is_empty(work_details):
    member_id = MemberId()
    work_id = str(uuid4())
    member_id = str(uuid4())
    uow = FakeUnitOfWork()
    with pytest.raises(work_service.InvalidDataError):
        work_service.add_work(
            uow=uow,
            work_id=work_id,
            title=work_details["title"],
            content="",
            age_restriction=work_details["age_restriction"],
            genre=work_details["genre"],
            member_id=member_id,
        )


def test_add_work_raises_member_exception_InvalidDataError_when_member_id_is_None(
    work_details
):
    work_id = str(uuid4())
    uow = FakeUnitOfWork()
    with pytest.raises(work_service.InvalidDataError):
        work_service.add_work(
            uow=uow,
            work_id=work_id,
            title=work_details["title"],
            content=work_details["content"],
            age_restriction=work_details["age_restriction"],
            genre=work_details["genre"],
            member_id="",
        )


def test_list_works(work_details):
    work_id = str(uuid4())
    member_id = str(uuid4())
    work_id_2 = str(uuid4())
    member_id_2 = str(uuid4())
    uow = FakeUnitOfWork()
    work_1 = work_service.add_work(
        uow=uow,
        work_id=work_id,
        title=work_details["title"],
        content=work_details["content"],
        age_restriction=work_details["age_restriction"],
        genre=work_details["genre"],
        member_id=member_id,
    )
    work_2 = work_service.add_work(
        uow=uow,
        work_id=work_id_2,
        title=work_details["title"],
        content=work_details["content"],
        age_restriction=work_details["age_restriction"],
        genre=work_details["genre"],
        member_id=member_id_2,
    )
    works = work_service.list_works(uow=uow)
    assert len(works) == 2
    assert work_1 in works
    assert work_2 in works


def test_list_works_returns_empty_list_when_no_works_exist():
    uow = FakeUnitOfWork()
    works = work_service.list_works(uow=uow)
    assert len(works) == 0
    assert works == []
