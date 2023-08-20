# Description: Tests for the Rating class
from datetime import datetime
from uuid import uuid4

import pytest
from pytest import raises

from critique_wheel.domain.models.rating import MissingEntryError, Rating, RatingStatus


@pytest.fixture
def test_rating():
    return Rating.create(
        score=4,
        comment="This is a comment.",
        member_id=45,
        critique_id=42,
    )


@pytest.fixture
def test_rating_no_comment():
    return Rating.create(
        score=4,
        comment="",
        member_id=45,
        critique_id=42,
    )


# Test Creation of Rating with Valid Score:
def test_ensure_a_rating_can_be_created_with_a_valid_score():
    rating = Rating.create(
        score=4,
        comment="This is a comment.",
        member_id=45,
        critique_id=42,
    )
    assert rating.score == 4
    assert rating.comment == "This is a comment."
    assert rating.status == RatingStatus.ACTIVE
    assert rating.member_id == 45
    assert rating.critique_id == 42


# Test Creation of Rating with out member_id
def test_ensure_a_rating_can_be_created_with_a_valid_score_and_no_comment():
    rating = Rating.create(
        score=4,
        comment="",
        member_id=45,
        critique_id=42,
    )
    assert rating.score == 4
    assert rating.comment == ""
    assert rating.status == RatingStatus.ACTIVE
    assert rating.member_id == 45
    assert rating.critique_id == 42


# Test Creation of Rating without critique_id
def test_ensure_a_rating_cannot_be_created_without_critique_id():
    with raises(MissingEntryError):
        Rating.create(
            score=4,
            comment="This is a comment.",
            member_id=45,
            critique_id=None,
        )


# Test Creation of Rating with Invalid Score:
def test_ensure_a_rating_cannot_be_created_without_member_id():
    with raises(MissingEntryError):
        Rating.create(
            score=4,
            comment="This is a comment.",
            member_id=None,
            critique_id=42,
        )


# Test Creation of Rating with Invalid Score:
def test_ensure_a_rating_cannot_be_created_with_an_invalid_score():
    with raises(ValueError, match="Score must be between 1 and 5."):
        Rating.create(
            score=6,
            comment="This is a comment.",
            member_id=45,
            critique_id=42,
        )

    with raises(ValueError, match="Score must be between 1 and 5."):
        Rating.create(
            score=0,
            comment="This is a comment.",
            member_id=45,
            critique_id=42,
        )

    with raises(ValueError, match="Score must be between 1 and 5."):
        Rating.create(
            score="Stars are not a valid rating.",
            comment="This is a comment.",
            member_id=45,
            critique_id=42,
        )


# Test Updating Rating Score:
def test_ensure_a_rating_s_score_can_be_updated(test_rating):
    rating = test_rating
    assert rating.score == 4
    rating.update_score(5)
    assert rating.score == 5


# Test Preventing Update of Associated Critique:
def test_ensure_the_associated_critique_of_a_rating_cannot_be_changed(test_rating):
    rating = test_rating
    assert rating.critique_id == 42
    with raises(AttributeError, match="Can't set attribute"):
        rating.critique_id = 43


# Test Preventing Update of Associated Member:
def test_ensure_the_associated_member_of_a_rating_cannot_be_changed(test_rating):
    rating = test_rating
    assert rating.member_id == 45
    with raises(AttributeError, match="Can't set attribute"):
        rating.member_id = 43


# Test Optional Comment on Rating:
def test_ensure_a_comment_can_be_added_to_a_rating(test_rating_no_comment):
    rating = test_rating_no_comment
    assert rating.comment == ""
    rating.add_comment("This is a comment.")
    assert rating.comment == "This is a comment."


# Test Mark Critique as ACTIVE:
def test_ensure_a_critique_status_can_be_marked_archived(test_rating):
    rating = test_rating
    assert rating.status == RatingStatus.ACTIVE
    rating.archive()
    assert rating.status == RatingStatus.ARCHIVED


# Test Mark Critique as ACTIVE:
def test_ensure_a_critique_status_can_be_marked_as_active(test_rating):
    rating = test_rating
    rating.mark_pending_review()
    assert rating.status == RatingStatus.PENDING_REVIEW
    rating.approve()
    assert rating.status == RatingStatus.ACTIVE

    rating.reject()
    assert rating.status == RatingStatus.REJECTED
    rating.approve()
    assert rating.status == RatingStatus.ACTIVE

    rating.mark_for_deletion()
    assert rating.status == RatingStatus.MARKED_FOR_DELETION
    rating.approve()
    assert rating.status == RatingStatus.ACTIVE


# Test Mark Critique as Pending Review:
def test_ensure_a_critique_status_can_be_marked_as_pending_review(test_rating):
    rating = test_rating
    assert rating.status == RatingStatus.ACTIVE
    rating.mark_pending_review()
    assert rating.status == RatingStatus.PENDING_REVIEW


# Test Mark Critique as Marked for Deletion:
def test_ensure_a_critique_status_can_be_marked_for_deletion(test_rating):
    rating = test_rating
    assert rating.status == RatingStatus.ACTIVE
    rating.mark_for_deletion()
    assert rating.status == RatingStatus.MARKED_FOR_DELETION


# Test Rejection of Rating:
def test_ensure_a_rating_can_be_rejected(test_rating):
    rating = test_rating
    assert rating.status == RatingStatus.ACTIVE
    rating.reject()
    assert rating.status == RatingStatus.REJECTED


# Test Restore Critique:
def test_ensure_a_critique_status_can_be_restored_to_active(test_rating):
    rating = test_rating
    rating.mark_pending_review()
    assert rating.status == RatingStatus.PENDING_REVIEW
    rating.restore()
    assert rating.status == RatingStatus.ACTIVE

    rating.reject()
    assert rating.status == RatingStatus.REJECTED
    rating.restore()
    assert rating.status == RatingStatus.ACTIVE

    rating.mark_for_deletion()
    assert rating.status == RatingStatus.MARKED_FOR_DELETION
    rating.restore()
    assert rating.status == RatingStatus.ACTIVE
