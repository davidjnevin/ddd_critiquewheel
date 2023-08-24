from datetime import datetime
from uuid import uuid4

import pytest

from critique_wheel.domain.models.work import (
    MissingEntryError,
    Work,
    WorkAgeRestriction,
    WorkGenre,
    WorkStatus,
)


def test_create_work_with_valid_data():
    title = "Sample Work"
    content = "This is a sample fictional work for testing."
    work = Work.create(
        title=title,
        content=content,
        age_restriction=WorkAgeRestriction.ADULT,
        genre=WorkGenre.OTHER,
        member_id=uuid4(),
    )

    assert work.title == title
    assert work.content == content
    assert work.word_count == len(content.split())
    assert work.status == WorkStatus.PENDING_REVIEW
    assert work.age_restriction == WorkAgeRestriction.ADULT
    assert work.genre == WorkGenre.OTHER
    assert work.member_id is not None
    assert work.submission_date is not None


def test_create_work_without_title():
    with pytest.raises(MissingEntryError):
        Work.create(
            title="",
            content="Valid content",
            age_restriction=WorkAgeRestriction.ADULT,
            genre=WorkGenre.OTHER,
            member_id=uuid4(),
        )


def test_create_work_without_content():
    with pytest.raises(MissingEntryError):
        Work.create(
            title="Valid Title",
            content="",
            age_restriction=WorkAgeRestriction.ADULT,
            genre=WorkGenre.OTHER,
            member_id=uuid4(),
        )


def test_create_work_without_genre():
    with pytest.raises(MissingEntryError):
        Work.create(
            title="Valid Title",
            content="valid content",
            age_restriction=WorkAgeRestriction.ADULT,
            genre=None, # type: ignore
            member_id=uuid4(),
        )


def test_create_work_without_age_restriction():
    with pytest.raises(MissingEntryError):
        Work.create(
            title="Valid Title",
            content="Valid content",
            age_restriction=None,  # type: ignore
            genre=WorkGenre.OTHER,
            member_id=uuid4(),
        )


def test_create_work_without_member_id():
    with pytest.raises(MissingEntryError):
        Work.create(
            title="Valid Title",
            content="Valid content",
            age_restriction=None, # type: ignore
            genre=WorkGenre.OTHER,
            member_id=None,
        )


def test_word_count_calculation():
    content = "This is a test content with eight words."
    work = Work.create(
        title="Test Title",
        content=content,
        age_restriction=WorkAgeRestriction.ADULT,
        genre=WorkGenre.OTHER,
        member_id=uuid4(),
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
