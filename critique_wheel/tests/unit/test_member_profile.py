from uuid import uuid4

import pytest

from critique_wheel.domain.models.member_profile import MemberProfile

# Mock data for testing
MOCK_MEMBER_ID = "12345"
VALID_FIRST_NAME = "John"
VALID_LAST_NAME = "Doe"
VALID_BIO = "This is a sample bio with less than 200 words."
INVALID_BIO = "This is " + "a " * 201 + "bio."


@pytest.fixture
def member_profile():
    return MemberProfile.create(
        member_id=uuid4(),
        first_name="David",
        last_name="Smith",
        bio="This is a sample bio with less than 200 words.",
        visible=True,
    )


class TestMemberProfile:
    def test_create_valid_profile(self):
        member = MemberProfile.create(
            member_id=uuid4(),
            first_name="David",
            last_name="Smith",
            bio="This is a sample bio with less than 200 words.",
            visible=True,
        )
        assert member.first_name == "David"
        assert member.last_name == "Smith"
        assert member.bio == "This is a sample bio with less than 200 words."
        assert member.visibility == True
        assert member.id is not None

    def test_create_invalid_name(self):
        with pytest.raises(ValueError):
            MemberProfile.create(
                member_id=MOCK_MEMBER_ID,
                first_name="a" * 51,
                last_name=VALID_LAST_NAME,
                bio=VALID_BIO,
            )

    def test_create_invalid_bio(self):
        with pytest.raises(ValueError):
            MemberProfile.create(
                MOCK_MEMBER_ID,
                VALID_FIRST_NAME,
                VALID_LAST_NAME,
                INVALID_BIO,
            )


    def test_change_first_name(self, member_profile):
        profile = member_profile
        new_name = "Jane"
        profile.change_first_name(new_name)
        assert profile.first_name == new_name

    def test_change_last_name(self, member_profile):
        profile = member_profile
        new_name = "Smithy"
        profile.change_last_name(new_name)
        assert profile.last_name == new_name

    def test_change_bio(self, member_profile):
        profile = member_profile
        new_bio = "This is a new bio."
        profile.change_bio(new_bio)
        assert profile.bio == new_bio

    def test_toggle_visibility(self, member_profile):
        profile = member_profile
        initial_visibility = profile.visibility
        profile.toggle_visibility()
        assert profile.visibility != initial_visibility
