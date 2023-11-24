import os
from uuid import uuid4
from critique_wheel.members.value_objects import MemberId, FirstName, LastName, Bio, Visibility

class MemberProfile:
    def __init__(
        self,
        member_id: MemberId,
        first_name: FirstName,
        last_name: LastName,
        bio: Bio = Bio(""),
        visible: Visibility = Visibility(True),
        profile_id =None,  # This is only used for testing
    ):
        self.id = uuid4() or profile_id  # Unique identifier for the profile
        self.member_id = member_id
        self.first_name = first_name
        self.last_name = last_name
        self.bio = bio
        self.visibility = visible

    @classmethod
    def create(
        cls,
        member_id: MemberId,
        first_name: FirstName,
        last_name: LastName,
        bio: Bio,
        visible: Visibility = Visibility(True),
    ):
        # Validate first and last names
        # cls._validate_name(first_name)
        # cls._validate_name(last_name)
        # cls._validate_bio(bio)
        return cls(
            member_id=member_id,
            first_name=first_name,
            last_name=last_name,
            bio=bio,
            visible=visible,
        )

    def change_first_name(self, new_first_name: FirstName):
        # self._validate_name(new_first_name)
        self.first_name = new_first_name

    def change_last_name(self, new_last_name: LastName):
        # self._validate_name(new_last_name)
        self.last_name = new_last_name

    def change_bio(self, new_bio: Bio):
        # self._validate_bio(new_bio)
        self.bio = new_bio

    def toggle_visibility(self):
        self.visibility = not self.visibility
