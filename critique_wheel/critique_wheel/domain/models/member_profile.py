import os
from uuid import uuid4


class MemberProfile:
    def __init__(
        self,
        member_id,
        first_name,
        last_name,
        bio="",
        visible=True,
        profile_id=None,  # This is only used for testing
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
        member_id,
        first_name,
        last_name,
        bio,
        visible=True,
    ):
        # Validate first and last names
        cls._validate_name(first_name)
        cls._validate_name(last_name)
        cls._validate_bio(bio)
        return cls(
            member_id=member_id,
            first_name=first_name,
            last_name=last_name,
            bio=bio,
            visible=visible,
        )

    def change_first_name(self, new_first_name):
        self._validate_name(new_first_name)
        self.first_name = new_first_name

    def change_last_name(self, new_last_name):
        self._validate_name(new_last_name)
        self.last_name = new_last_name

    def change_bio(self, new_bio):
        self._validate_bio(new_bio)
        self.bio = new_bio

    @staticmethod
    def _validate_name(name):
        if len(name) > 50:
            raise ValueError("Name must be under 50 characters.")

    @staticmethod
    def _validate_bio(bio):
        if len(bio.split()) > 200 or len(bio) > 1200:
            raise ValueError("Bio must be under 200 words and 1200 characters.")

    @staticmethod
    def _validate_bio_photo_format(bio_photo):
        valid_extensions = [".jpg", ".jpeg", ".png"]
        _, extension = os.path.splitext(bio_photo)
        if extension not in valid_extensions:
            raise ValueError(f"Invalid file type. Allowed types are: {', '.join(valid_extensions)}")

    def toggle_visibility(self):
        self.visibility = not self.visibility
