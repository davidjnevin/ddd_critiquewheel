# Throwaway test file for testing ORM functionality

import pytest
from critique_wheel.domain.models.critique import Critique
from critique_wheel.domain.models.work import Work
from critique_wheel.domain.models.rating import Rating
from critique_wheel.domain.models.credit import CreditManager, TransactionType
from critique_wheel.domain.models.IAM import Member, MemberRole, MemberStatus


# @pytest.mark.skip(reason="Throwaway test file for testing ORM functionality")
class TestOrm:
    @pytest.mark.skip(reason="Throwaway test file for testing ORM functionality")
    def test_create_and_retrieve_member(self, session, valid_member):
        # Arrange
        new_member = valid_member

        # Act
        session.add(new_member)
        session.commit()
        retrieved_member = session.query(Member).filter_by(username="test_username").one()

        # Assert
        assert retrieved_member.id == new_member.id
        assert retrieved_member.email == new_member.email
        assert retrieved_member.password != "secure_unguessable_password"

    @pytest.mark.skip(reason="Throwaway test file for testing ORM functionality")
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


    @pytest.mark.skip(reason="Throwaway test file for testing ORM functionality")
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

    @pytest.mark.skip(reason="Throwaway test file for testing ORM functionality")
    def test_create_and_retreive_rating(self, session, valid_rating):
        # Arrange
        new_rating = valid_rating

        # Act
        session.add(new_rating)
        session.commit()
        retrieved_rating = session.query(Rating).filter_by(score=5).one()

        # Assert
        assert retrieved_rating.id == new_rating.id
        assert retrieved_rating.member_id == new_rating.member_id
        assert retrieved_rating.score == 5

    @pytest.mark.skip(reason="Throwaway test file for testing ORM functionality")
    def test_create_and_retreive_credit(self, session, valid_credit):
        # Arrange
        new_credit = valid_credit

        # Act
        session.add(new_credit)
        session.commit()
        retrieved_credit = session.query(CreditManager).filter_by(amount=5).one()

        # Assert
        assert retrieved_credit.id == new_credit.id
        assert retrieved_credit.member_id == new_credit.member_id
        assert retrieved_credit.amount == 5
        assert retrieved_credit.transaction_type == TransactionType.CRITIQUE_GIVEN
        assert retrieved_credit.work_id == new_credit.work_id
