import os
from uuid import uuid4


class MemberProfile:
    def __init__(
        self,
        member_id,
        first_name,
        last_name,
        bio="",
        bio_photo=None,
        visible=True,
        profile_id=None,  # This is only used for testing
    ):
        self.id = uuid4() or profile_id  # Unique identifier for the profile
        self.member_id = member_id
        self.first_name = first_name
        self.last_name = last_name
        self.bio = bio
        self.bio_photo = bio_photo
        self.visibility = visible

    @classmethod
    def create(
        cls,
        member_id,
        first_name,
        last_name,
        bio,
        bio_photo,
        visible=True,
    ):
        # Validate first and last names
        cls._validate_name(first_name)
        cls._validate_name(last_name)
        cls._validate_bio(bio)
        cls._validate_bio_photo_format(bio_photo)
        # cls._validate_bio_photo_size(bio_photo)
        return cls(
            member_id=member_id,
            first_name=first_name,
            last_name=last_name,
            bio=bio,
            bio_photo=bio_photo,
            visible=visible,
        )

        # TODO: Save the bio_photo to the desired location

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

    @staticmethod
    def _validate_bio_photo_size(bio_photo):
        # Calculate size in bytes

        if bio_photo.size > 2 * 1024 * 1024:  # 2MB
            raise ValueError("Bio photo must be under 2MB.")
        # TODO: Add dimension checks for the bio photo if necessary

    def upload_bio_photo(self, photo):
        return NotImplemented
        self.bio_photo = photo

    def toggle_visibility(self):
        self.visibility = not self.visibility
