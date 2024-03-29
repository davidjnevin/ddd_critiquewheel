# Description: This file contains the unit tests for the Critique model.
from datetime import datetime, timedelta

import pytest
from pytest import raises

from critique_wheel.critiques.models.critique import (
    Critique,
    CritiqueStatus,
    MissingEntryError,
)
from critique_wheel.critiques.value_objects import (
    CritiqueAbout,
    CritiqueIdeas,
    CritiqueSuccesses,
    CritiqueWeaknesses,
)
from critique_wheel.members.value_objects import MemberId
from critique_wheel.works.models.work import WorkStatus
from critique_wheel.works.value_objects import WorkId

text_longer_than_40_words = "words " * 45


# Test Creation of Critique with All Required Content
def test_ensure_a_critique_can_be_created_with_all_required_content_elements(
    valid_rating, another_valid_rating, valid_work, active_valid_member
):
    new_rating = valid_rating
    another_rating = another_valid_rating
    new_work = valid_work
    new_member = active_valid_member
    critique = Critique.create(
        critique_about=CritiqueAbout(text_longer_than_40_words),
        critique_successes=CritiqueSuccesses(text_longer_than_40_words),
        critique_weaknesses=CritiqueWeaknesses(text_longer_than_40_words),
        critique_ideas=CritiqueIdeas(text_longer_than_40_words),
        member_id=new_member.id,
        work_id=new_work.id,
    )
    critique.add_rating(new_rating)
    critique.add_rating(another_rating)

    assert str(critique.critique_about) == text_longer_than_40_words
    assert str(critique.critique_successes) == text_longer_than_40_words
    assert str(critique.critique_weaknesses) == text_longer_than_40_words
    assert str(critique.critique_ideas) == text_longer_than_40_words
    assert critique.member_id == new_member.id
    assert critique.work_id == new_work.id
    assert critique.ratings == [new_rating, another_rating] == critique.list_ratings()
    assert critique.id is not None


# Test Creation of Critique with Missing Content:
def test_ensure_a_critique_cannot_be_created_if_about_is_empty():
    with raises(MissingEntryError):
        Critique.create(
            critique_about=CritiqueAbout(""),
            critique_successes=CritiqueSuccesses(text_longer_than_40_words),
            critique_weaknesses=CritiqueWeaknesses(text_longer_than_40_words),
            critique_ideas=CritiqueIdeas(text_longer_than_40_words),
            member_id=MemberId(),
            work_id=WorkId(),
        )


def test_ensure_a_critique_cannot_be_created_if_successes_is_empty():
    with raises(MissingEntryError):
        Critique.create(
            critique_about=CritiqueAbout(text_longer_than_40_words),
            critique_successes=CritiqueSuccesses(""),
            critique_weaknesses=CritiqueWeaknesses(text_longer_than_40_words),
            critique_ideas=CritiqueIdeas(text_longer_than_40_words),
            member_id=MemberId(),
            work_id=WorkId(),
        )


def test_ensure_a_critique_cannot_be_created_if_weaknesses_is_empty():
    with raises(MissingEntryError):
        Critique.create(
            critique_about=CritiqueAbout(text_longer_than_40_words),
            critique_successes=CritiqueSuccesses(text_longer_than_40_words),
            critique_weaknesses=CritiqueWeaknesses(""),
            critique_ideas=CritiqueIdeas(text_longer_than_40_words),
            member_id=MemberId(),
            work_id=WorkId(),
        )


def test_ensure_a_critique_cannot_be_created_if_ideas_is_empty():
    with raises(MissingEntryError):
        Critique.create(
            critique_about=CritiqueAbout(text_longer_than_40_words),
            critique_successes=CritiqueSuccesses(text_longer_than_40_words),
            critique_weaknesses=CritiqueWeaknesses(text_longer_than_40_words),
            critique_ideas=CritiqueIdeas(""),
            member_id=MemberId(),
            work_id=WorkId(),
        )


def test_ensure_a_critique_cannot_be_created_if_member_id_is_empty():
    with raises(MissingEntryError):
        Critique.create(
            critique_about=CritiqueAbout(text_longer_than_40_words),
            critique_successes=CritiqueSuccesses(text_longer_than_40_words),
            critique_weaknesses=CritiqueWeaknesses(text_longer_than_40_words),
            critique_ideas=CritiqueIdeas(text_longer_than_40_words),
            member_id=None,
            work_id=WorkId(),
        )


def test_ensure_a_critique_cannot_be_created_if_work_id_is_empty():
    with raises(MissingEntryError):
        Critique.create(
            critique_about=CritiqueAbout(text_longer_than_40_words),
            critique_successes=CritiqueSuccesses(text_longer_than_40_words),
            critique_weaknesses=CritiqueWeaknesses(text_longer_than_40_words),
            critique_ideas=CritiqueIdeas(text_longer_than_40_words),
            member_id=MemberId(),
            work_id=None,
        )


# Test Setting Submission Date on Critique Creation:
def test_ensure_the_submission_date_is_set_when_a_critique_is_submitted(
    valid_critique, valid_work
):
    critique = valid_critique
    valid_work.status = WorkStatus.ACTIVE
    valid_work.add_critique(critique)
    assert critique.submission_date.date() == datetime.today().date()


# Test Approving Critique Content:
def test_ensure_the_last_updated_date_is_set_when_a_critique_s_content_is_approved(
    valid_critique,
):
    critique = valid_critique
    critique.last_updated_date = datetime.now() - timedelta(days=1)
    critique.status = CritiqueStatus.PENDING_REVIEW
    critique.approve()
    assert critique.status == CritiqueStatus.ACTIVE
    assert critique.last_updated_date.date() == datetime.today().date()


# Test Archiving a Critique:
def test_ensure_a_critique_can_be_archived_and_its_status_and_archive_date_are_updated(
    valid_critique,
):
    critique = valid_critique
    critique.last_updated_date = datetime.now() - timedelta(days=1)
    critique.archive()

    assert critique.status == CritiqueStatus.ARCHIVED
    assert critique.archive_date is not None
    assert critique.last_updated_date.date() == datetime.today().date()


# Test Marking a Critique for Deletion:
def test_ensure_a_critique_can_be_marked_for_deletion_and_its_status_is_updated(
    valid_critique,
):
    critique = valid_critique
    critique.last_updated_date = datetime.now() - timedelta(days=1)
    critique.mark_for_deletion()

    assert critique.status == CritiqueStatus.MARKED_FOR_DELETION
    assert critique.last_updated_date.date() == datetime.today().date()


# Test Marking a Critique as Pending Review:
def test_ensure_a_critique_can_be_marked_as_pending_review_and_its_status_is_updated(
    valid_critique,
):
    critique = valid_critique
    critique.last_updated_date = datetime.now() - timedelta(days=1)
    critique.pending_review()

    assert critique.status == CritiqueStatus.PENDING_REVIEW
    assert critique.last_updated_date.date() == datetime.today().date()


# Test Rejecting a Critique:
def test_ensure_a_critique_can_be_rejected_and_its_status_is_updated(valid_critique):
    critique = valid_critique
    critique.last_updated_date = datetime.now() - timedelta(days=1)
    critique.reject()

    assert critique.status == CritiqueStatus.REJECTED
    assert critique.last_updated_date.date() == datetime.today().date()
    # TODO: This will have an effect on rating and credits.


# Test Restoring an Archived Critique:
def test_ensure_an_archived_critique_can_be_restored_to_active_status_and_its_archive_date_is_cleared(
    valid_critique,
):
    critique = valid_critique
    critique.last_updated_date = datetime.now() - timedelta(days=1)
    critique.archive()
    assert critique.last_updated_date.date() == datetime.today().date()
    critique.restore()

    assert critique.status == CritiqueStatus.ACTIVE
    assert critique.last_updated_date.date() == datetime.today().date()


def test_add_rating(valid_critique, valid_rating):
    critique = valid_critique
    critique.last_updated_date = datetime.now() - timedelta(days=1)
    rating = valid_rating
    critique.add_rating(rating)
    assert critique.last_updated_date.date() == datetime.today().date()
    assert critique.ratings == [rating]


def test_connot_add_the_same_rating_twice(another_valid_rating, valid_critique):
    critique = valid_critique
    critique.last_updated_date = datetime.now() - timedelta(days=1)
    critique.ratings = []
    rating = another_valid_rating
    critique.add_rating(rating)
    with pytest.raises(ValueError):
        critique.add_rating(rating)


# def test_cannot_add_critique_to_non_active_work(valid_work):
#     work = valid_work
#     work.status = WorkStatus.PENDING_REVIEW
#     with pytest.raises(
#         WorkNotAvailableForCritiqueError,
#         match="This work is not available for critique",
#     ):
#         work.add_critique("critique3")
