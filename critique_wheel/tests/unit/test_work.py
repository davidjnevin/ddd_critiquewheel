from datetime import datetime

import pytest

from critique_wheel.domain.models.work import (
    CritiqueDuplicateError,
    MissingEntryError,
    Work,
    WorkAgeRestriction,
    WorkGenre,
    WorkNotAvailableForCritiqueError,
    WorkStatus,
)
from critique_wheel.members.value_objects import MemberId
from critique_wheel.works.value_objects import Content, Title


def test_create_work_with_valid_data():
    title_text = "Sample Work"
    content_text = "This is a sample fictional work for testing."
    work = Work.create(
        title=Title(title_text),
        content=Content(content_text),
        age_restriction=WorkAgeRestriction.ADULT,
        genre=WorkGenre.OTHER,
        member_id=MemberId(),
        critiques=["critique1", "critique2"],
    )

    assert str(work.title) == title_text
    assert str(work.content) == content_text
    assert work.word_count == len(content_text.split())
    assert work.status == WorkStatus.PENDING_REVIEW
    assert work.age_restriction == WorkAgeRestriction.ADULT
    assert work.genre == WorkGenre.OTHER
    assert work.member_id is not None
    assert work.submission_date is not None
    assert work.critiques == ["critique1", "critique2"]


def test_create_work_without_title():
    with pytest.raises(MissingEntryError):
        Work.create(
            title=Title(""),
            content=Content("Valid content"),
            age_restriction=WorkAgeRestriction.ADULT,
            genre=WorkGenre.OTHER,
            member_id=MemberId(),
        )


def test_create_work_without_content():
    with pytest.raises(MissingEntryError):
        Work.create(
            title=Title("Valid Title"),
            content=Content(""),
            age_restriction=WorkAgeRestriction.ADULT,
            genre=WorkGenre.OTHER,
            member_id=MemberId(),
        )


def test_create_work_without_genre():
    with pytest.raises(MissingEntryError):
        Work.create(
            title=Title("Valid Title"),
            content=Content("valid content"),
            age_restriction=WorkAgeRestriction.ADULT,
            genre=None,  # type: ignore
            member_id=MemberId(),
        )


def test_create_work_without_age_restriction():
    with pytest.raises(MissingEntryError):
        Work.create(
            title=Title("Valid Title"),
            content=Content("Valid content"),
            age_restriction=None,  # type: ignore
            genre=WorkGenre.OTHER,
            member_id=MemberId(),
        )


def test_create_work_without_member_id():
    with pytest.raises(MissingEntryError):
        Work.create(
            title=Title("Valid Title"),
            content=Content("Valid content"),
            age_restriction=None,  # type: ignore
            genre=WorkGenre.OTHER,
            member_id=MemberId(None),
        )


def test_list_critiques(valid_work_with_two_critiques):
    work = valid_work_with_two_critiques
    assert work.list_critiques() == ["critique1", "critique2"]


def test_add_critique(valid_work_with_two_critiques):
    work = valid_work_with_two_critiques
    work.status = WorkStatus.ACTIVE
    work.add_critique("critique3")
    assert work.critiques == ["critique1", "critique2", "critique3"]


def test_cannot_add_critique_to_non_active_work(valid_work):
    work = valid_work
    work.status = WorkStatus.PENDING_REVIEW
    with pytest.raises(
        WorkNotAvailableForCritiqueError,
        match="This work is not available for critique",
    ):
        work.add_critique("critique3")


def test_cannot_add_same_critique_twice(valid_work_with_two_critiques):
    work = valid_work_with_two_critiques
    work.status = WorkStatus.ACTIVE
    with pytest.raises(
        CritiqueDuplicateError,
        match="Critique already exists",
    ):
        work.add_critique("critique1")


def test_word_count_calculation():
    content = "This is a test content with eight words."
    work = Work.create(
        title=Title("Test Title"),
        content=Content(content),
        age_restriction=WorkAgeRestriction.ADULT,
        genre=WorkGenre.OTHER,
        member_id=MemberId(),
    )

    assert work.word_count == 8


def test_submission_date_setting(valid_work):
    work = valid_work
    assert work.submission_date.date() == datetime.today().date()


def test_work_archiving(valid_work):
    work = valid_work
    work.archive()

    assert work.status == WorkStatus.ARCHIVED
    assert work.archive_date is not None


def test_work_rejected(valid_work):
    work = valid_work
    work.reject()

    assert work.status == WorkStatus.REJECTED


def test_work_approved(valid_work):
    work = valid_work
    work.approve()

    assert work.status == WorkStatus.ACTIVE


def test_work_marked_for_deletion(valid_work):
    work = valid_work
    work.mark_for_deletion()

    assert work.status == WorkStatus.MARKED_FOR_DELETION


def test_active_work_availability_for_critique(valid_work):
    work = valid_work
    work.approve()

    assert work.is_available_for_critique() is True


def test_non_active_work_availability_for_critique(valid_work):
    work = valid_work
    work.WorkStatus = WorkStatus.PENDING_REVIEW
    assert work.is_available_for_critique() is False

    work.archive()
    assert work.is_available_for_critique() is False

    work.mark_for_deletion()
    assert work.is_available_for_critique() is False

    work.reject()
    assert work.is_available_for_critique() is False


def test_archived_work_restoration(valid_work):
    work = valid_work
    work.archive()
    work.restore()

    assert work.status == WorkStatus.ACTIVE
    assert work.archive_date is None
