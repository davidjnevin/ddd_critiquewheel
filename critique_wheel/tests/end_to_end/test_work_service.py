from uuid import uuid4

import pytest

from critique_wheel.domain.services.work_service import (
    DuplicateWorkError,
    InvalidDataError,
)


def test_create_work(work_service, work_details):
    member_id = uuid4()
    work = work_service.create_work(
        title=work_details["title"],
        content=work_details["content"],
        age_restriction=work_details["age_restriction"],
        genre=work_details["genre"],
        member_id=member_id,
    )
    assert work.title == "Test Title"
    assert work.content == "Test content"
    assert work.member_id != None
    assert work.genre == "YOUNG ADULT"
    assert work.status == "PENDING REVIEW"
    assert work.age_restriction == "ADULT"
    assert work.critiques == []


def test_create_dupliacte_work_raises_DuplicateWorkError(work_service, work_details):
    member_id = uuid4()
    work_1 = work_service.create_work(
        title=work_details["title"],
        content=work_details["content"],
        age_restriction=work_details["age_restriction"],
        genre=work_details["genre"],
        member_id=member_id,
    )
    with pytest.raises(DuplicateWorkError):
        work_2 = work_service.create_work(
            work_id=work_1.id,
            title=work_details["title"],
            content=work_details["content"],
            age_restriction=work_details["age_restriction"],
            genre=work_details["genre"],
            member_id=member_id,
        )


@pytest.mark.current
def test_create_work_raises_InvalidDataError_when_title_is_empty(work_service, work_details):
    member_id = uuid4()
    with pytest.raises(InvalidDataError):
        work = work_service.create_work(
            title="",
            content=work_details["content"],
            age_restriction=work_details["age_restriction"],
            genre=work_details["genre"],
            member_id=member_id,
        )


@pytest.mark.current
def test_create_work_raises_InvalidDataError_when_content_is_empty(work_service, work_details):
    member_id = uuid4()
    with pytest.raises(InvalidDataError):
        work = work_service.create_work(
            title=work_details["title"],
            content="",
            age_restriction=work_details["age_restriction"],
            genre=work_details["genre"],
            member_id=member_id,
        )
@pytest.mark.current
def test_create_work_raises_InvalidDataError_when_member_id_is_None(work_service, work_details):
    member_id = None
    with pytest.raises(InvalidDataError):
        work = work_service.create_work(
            title=work_details["title"],
            content=work_details["content"],
            age_restriction=work_details["age_restriction"],
            genre=work_details["genre"],
            member_id=member_id,
        )


def test_list_works(work_service, work_details):
    member_id = uuid4()
    work_1 = work_service.create_work(
        title=work_details["title"],
        content=work_details["content"],
        age_restriction=work_details["age_restriction"],
        genre=work_details["genre"],
        member_id=member_id,
    )
    work_2 = work_service.create_work(
        title=work_details["title"],
        content=work_details["content"],
        age_restriction=work_details["age_restriction"],
        genre=work_details["genre"],
        member_id=member_id,
    )
    works = work_service.list_works()
    assert len(works) == 2
    assert work_1 in works
    assert work_2 in works


def test_list_works_returns_empty_list_when_no_works_exist(work_service):
    works = work_service.list_works()
    assert len(works) == 0
    assert works == []
