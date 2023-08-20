# Description: This file contains the unit tests for the Critique model.
from datetime import datetime
from uuid import uuid4

import pytest
from pytest import raises

from critique_wheel.domain.models.critique import (
    Critique,
    CritiqueStatus,
    MissingEntryError,
)


@pytest.fixture
def test_critique():
    return Critique.create(
        content_about="This is a test critique.",
        content_successes="This is a test critique.",
        content_weaknesses="This is a test critique.",
        content_ideas="This is a test critique.",
        member_id=uuid4(),
        work_id=uuid4(),
    )


# Test Creation of Critique with All Required Content
def test_ensure_a_critique_can_be_created_with_all_required_content_elements():
    critique = Critique.create(
        content_about="This is a test critique.",
        content_successes="This is a test critique.",
        content_weaknesses="This is a test critique.",
        content_ideas="This is a test critique.",
        member_id=uuid4(),
        work_id=uuid4(),
    )
    assert critique.content_about == "This is a test critique."
    assert critique.content_successes == "This is a test critique."
    assert critique.content_weaknesses == "This is a test critique."
    assert critique.content_ideas == "This is a test critique."


# Test Creation of Critique with Missing Content:
def test_ensure_a_critique_cannot_be_created_if_about_is_empty():
    with raises(MissingEntryError):
        Critique.create(
            content_about="",
            content_successes="This is a test critique.",
            content_weaknesses="This is a test critique.",
            content_ideas="This is a test critique.",
            member_id=uuid4(),
            work_id=uuid4(),
        )


def test_ensure_a_critique_cannot_be_created_if_successes_is_empty():
    with raises(MissingEntryError):
        Critique.create(
            content_about="This is a test critique.",
            content_successes="",
            content_weaknesses="This is a test critique.",
            content_ideas="This is a test critique.",
            member_id=uuid4(),
            work_id=uuid4(),
        )


def test_ensure_a_critique_cannot_be_created_if_weaknesses_is_empty():
    with raises(MissingEntryError):
        Critique.create(
            content_about="This is a test critique.",
            content_successes="This is a test critique.",
            content_weaknesses="",
            content_ideas="This is a test critique.",
            member_id=uuid4(),
            work_id=uuid4(),
        )


def test_ensure_a_critique_cannot_be_created_if_ideas_is_empty():
    with raises(MissingEntryError):
        Critique.create(
            content_about="This is a test critique.",
            content_successes="This is a test critique.",
            content_weaknesses="This is a test critique.",
            content_ideas="",
            member_id=uuid4(),
            work_id=uuid4(),
        )


def test_ensure_a_critique_cannot_be_created_if_member_id_is_empty():
    with raises(MissingEntryError):
        Critique.create(
            content_about="This is a test critique.",
            content_successes="This is a test critique.",
            content_weaknesses="This is a test critique.",
            content_ideas="This is a test critique.",
            member_id=None,
            work_id=uuid4(),
        )


def test_ensure_a_critique_cannot_be_created_if_work_id_is_empty():
    with raises(MissingEntryError):
        Critique.create(
            content_about="This is a test critique.",
            content_successes="This is a test critique.",
            content_weaknesses="This is a test critique.",
            content_ideas="This is a test critique.",
            member_id=uuid4(),
            work_id=None,
        )


# Test Setting Submission Date on Critique Creation:
def test_ensure_the_submission_date_is_set_when_a_critique_is_submitted(test_critique):
    critique = test_critique
    assert critique.submission_date.date() == datetime.today().date()


# Test Updating Critique Content:
def test_ensure_the_last_updated_date_is_set_when_a_critique_s_content_is_updated(test_critique):
    critique = test_critique
    assert critique.last_updated_date.date() == datetime.today().date()


# Test Archiving a Critique:
def test_ensure_a_critique_can_be_archived_and_its_status_and_archive_date_are_updated(test_critique):
    critique = test_critique
    critique.archive()

    assert critique.status == CritiqueStatus.ARCHIVED
    assert critique.archive_date is not None


# Test Marking a Critique for Deletion:
def test_ensure_a_critique_can_be_marked_for_deletion_and_its_status_is_updated(test_critique):
    critique = test_critique
    critique.mark_for_deletion()

    assert critique.status == CritiqueStatus.MARKED_FOR_DELETION


# Test Marking a Critique as Pending Review:
def test_ensure_a_critique_can_be_marked_as_pending_review_and_its_status_is_updated(test_critique):
    critique = test_critique
    critique.pending_review()

    assert critique.status == CritiqueStatus.PENDING_REVIEW


# Test Rejecting a Critique:
def test_ensure_a_critique_can_be_rejected_and_its_status_is_updated(test_critique):
    critique = test_critique
    critique.reject()

    assert critique.status == CritiqueStatus.REJECTED
    # TODO: This will have an effect on rating and credits.


# Test Restoring an Archived Critique:
def test_ensure_an_archived_critique_can_be_restored_to_active_status_and_its_archive_date_is_cleared(test_critique):
    critique = test_critique
    critique.archive()
    critique.restore()

    assert critique.status == CritiqueStatus.ACTIVE
