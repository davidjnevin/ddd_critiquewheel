from datetime import datetime

import pytest
from critique_wheel.domain.models.work import (MissingEntryError, Work,
                                               WorkAgeRestriction, WorkGenre,
                                               WorkStatus)


@pytest.fixture
def test_work():
    return Work.create(
        title="Test Title", content="Test content", age_restriction=WorkAgeRestriction.ADULT, genre=WorkGenre.OTHER
    )


def test_create_work_with_valid_data():
    title = "Sample Work"
    content = "This is a sample fictional work for testing."
    work = Work.create(title=title, content=content, age_restriction=WorkAgeRestriction.ADULT, genre=WorkGenre.OTHER)

    assert work.title == title
    assert work.content == content
    assert work.word_count == len(content.split())
    assert work.status == WorkStatus.PENDING_REVIEW
    assert work.age_restriction == WorkAgeRestriction.ADULT
    assert work.genre == WorkGenre.OTHER
    assert work.submission_date is not None


def test_create_work_without_title():
    with pytest.raises(MissingEntryError):
        Work.create(title="", content="Valid content", age_restriction=WorkAgeRestriction.ADULT, genre=WorkGenre.OTHER)


def test_create_work_without_content():
    with pytest.raises(MissingEntryError):
        Work.create(title="Valid Title", content="", age_restriction=WorkAgeRestriction.ADULT, genre=WorkGenre.OTHER)


def test_create_work_without_genre():
    with pytest.raises(MissingEntryError):
        Work.create(title="Valid Title", content="", age_restriction=WorkAgeRestriction.ADULT, genre="")


def test_create_work_without_age_restriction():
    with pytest.raises(MissingEntryError):
        Work.create(title="Valid Title", content="", age_restriction="", genre=WorkGenre.OTHER)


def test_word_count_calculation():
    content = "This is a test content with eight words."
    work = Work.create(
        title="Test Title", content=content, age_restriction=WorkAgeRestriction.ADULT, genre=WorkGenre.OTHER
    )

    assert work.word_count == 8


def test_submission_date_setting(test_work):
    work = test_work
    assert work.submission_date.date() == datetime.today().date()


def test_work_archiving(test_work):
    work = test_work
    work.archive()

    assert work.status == WorkStatus.ARCHIVED
    assert work.archive_date is not None


def test_work_rejected(test_work):
    work = test_work
    work.reject()

    assert work.status == WorkStatus.REJECTED


def test_work_approved(test_work):
    work = test_work
    work.approve()

    assert work.status == WorkStatus.ACTIVE


def test_work_marked_for_deletion(test_work):
    work = test_work
    work.mark_for_deletion()

    assert work.status == WorkStatus.MARKED_FOR_DELETION


def test_active_work_availability_for_critique(test_work):
    work = test_work
    work.approve()

    assert work.is_available_for_critique() is True


def test_non_active_work_availability_for_critique(test_work):
    work = test_work
    work.WorkStatus = WorkStatus.PENDING_REVIEW
    assert work.is_available_for_critique() is False

    work.archive()
    assert work.is_available_for_critique() is False

    work.mark_for_deletion()
    assert work.is_available_for_critique() is False

    work.reject()
    assert work.is_available_for_critique() is False


def test_archived_work_restoration(test_work):
    work = test_work
    work.archive()
    work.restore()

    assert work.status == WorkStatus.ACTIVE
    assert work.archive_date is None
