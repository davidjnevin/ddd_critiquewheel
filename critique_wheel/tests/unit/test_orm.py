# Throwaway test file for testing ORM functionality

import pytest
from critique_wheel.domain.models.critique import Critique
from critique_wheel.domain.models.work import Work
from critique_wheel.domain.models.rating import Rating


# @pytest.mark.skip(reason="Throwaway test file for testing ORM functionality")
class TestOrm:
    def test_create_and_retrieve_work(self, session, valid_work):
        # Arrange
        new_work = valid_work

        # Act
        session.add(new_work)
        session.commit()
        retrieved_work = session.query(Work).filter_by(title="Test Title").one()

        # Assert
        assert retrieved_work.id == new_work.id
        assert retrieved_work.title == "Test Title"
        assert retrieved_work.content == "Test content"


    def test_create_and_retrieve_critique(self, session, valid_critique):
        # Arrange
        new_critique = valid_critique

        # Act
        session.add(new_critique)
        session.commit()
        retrieved_critique = session.query(Critique).filter_by(content_about="About content.").one()

        # Assert
        assert retrieved_critique.id == new_critique.id
        assert retrieved_critique.content_about == "About content."

    def test_create_and_retreive_rating(self, session, valid_rating):
        # Arrange
        new_rating = valid_rating

        # Act
        session.add(new_rating)
        session.commit()
        retrieved_rating = session.query(Rating).filter_by(score=5).one()

        # Assert
        assert retrieved_rating.id == new_rating.id
        assert retrieved_rating.score == 5

