from uuid import UUID, uuid4

import pytest

from critique_wheel.members.models import exceptions
from critique_wheel.members.models.member_profile import MemberProfile
from critique_wheel.members.value_objects import (
    Bio,
    FirstName,
    LastName,
    MemberId,
    Visibility,
)

# Mock data for testing
MOCK_MEMBER_ID: MemberId = MemberId(UUID("7a16f584-7bca-4676-9838-8fb17d722490"))
VALID_FIRST_NAME: FirstName = FirstName("John")
VALID_LAST_NAME: LastName = LastName("Doe")
VALID_BIO = Bio("This is a sample bio with less than 200 words.")
INVALID_BIO_STR = "This is " + "a " * 201 + "bio."


@pytest.fixture
def member_profile():
    return MemberProfile.create(
        member_id=MemberId(uuid4()),
        first_name=FirstName("David"),
        last_name=LastName("Smith"),
        bio=Bio("This is a sample bio with less than 200 words."),
        visible=Visibility(True),
    )


class TestMemberProfile:
    def test_create_valid_profile(self):
        member = MemberProfile.create(
            member_id=MemberId(uuid4()),
            first_name=FirstName("David"),
            last_name=LastName("Smith"),
            bio=Bio("This is a sample bio with less than 200 words."),
            visible=Visibility(True),
        )
        assert member.first_name == FirstName("David")
        assert member.last_name == LastName("Smith")
        assert member.bio == Bio("This is a sample bio with less than 200 words.")
        assert member.visibility == Visibility(True)
        assert member.id is not None

    def test_create_invalid_name(self):
        with pytest.raises(exceptions.InvalidEntryError):
            MemberProfile.create(
                member_id=MOCK_MEMBER_ID,
                first_name=FirstName("a" * 51),
                last_name=VALID_LAST_NAME,
                bio=VALID_BIO,
            )

    def test_create_invalid_bio(self):
        with pytest.raises(exceptions.InvalidEntryError):
            MemberProfile.create(
                MOCK_MEMBER_ID,
                VALID_FIRST_NAME,
                VALID_LAST_NAME,
                Bio(INVALID_BIO_STR),
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
