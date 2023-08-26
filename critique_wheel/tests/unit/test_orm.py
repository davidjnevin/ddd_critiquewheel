# Throwaway test file for testing ORM functionality
import pytest

from critique_wheel.domain.models.credit import CreditManager, TransactionType
from critique_wheel.domain.models.critique import Critique
from critique_wheel.domain.models.IAM import Member, MemberRole, MemberStatus
from critique_wheel.domain.models.rating import Rating
from critique_wheel.domain.models.work import (
    Work,
    WorkAgeRestriction,
    WorkGenre,
    WorkStatus,
)


@pytest.mark.skip(reason="Throwaway test file for testing ORM functionality")
class TestOrm:
    @pytest.mark.skip(reason="Throwaway test file for testing ORM functionality")
    def test_create_and_retrieve_member(self, session, valid_member, valid_work, valid_critique):
        # Arrange
        new_member = valid_member

        new_member.status = MemberStatus.ACTIVE
        new_member.add_work(valid_work)
        new_member.add_critique(valid_critique)

        # Act
        session.add(new_member)
        session.commit()
        retrieved_member = session.query(Member).filter_by(username="test_username").one()

        # Assert
        assert retrieved_member.id == new_member.id
        assert retrieved_member.email == new_member.email
        assert retrieved_member.password != "secure_unguessable_password"
        assert retrieved_member.username == "test_username"
        assert retrieved_member.member_type == MemberRole.MEMBER
        assert retrieved_member.status == MemberStatus.ACTIVE
        assert retrieved_member.works != []
        assert retrieved_member.critiques != []


    @pytest.mark.skip(reason="Throwaway test file for testing ORM functionality")
    def test_create_and_retrieve_work(self, session, id_critique1, id_critique2, valid_member, valid_work):
        # Arrange
        # Arrange work
        assert valid_work.critiques == []
        new_work = valid_work
        new_work.status = WorkStatus.ACTIVE
        # Arrange critiques
        new_critique_1 = id_critique1
        new_critique_1.work_id = new_work.id
        new_critique_2 = id_critique2
        new_critique_2.work_id = new_work.id
        # TODO: Does this add_critique break my pure work model?
        new_work.add_critique(new_critique_1)
        new_work.add_critique(new_critique_2)
        # Arrange member
        new_member = valid_member
        new_work.member_id = new_member.id
        # Act
        session.add(new_work)
        session.commit()
        retrieved_work = session.query(Work).filter_by(title="Test Title").one()

        # Assert
        assert retrieved_work.id == new_work.id
        assert retrieved_work.title == "Test Title"
        assert retrieved_work.content == "Test content"
        assert retrieved_work.age_restriction == WorkAgeRestriction.ADULT
        assert retrieved_work.genre == WorkGenre.OTHER
        assert retrieved_work.status == WorkStatus.ACTIVE
        assert retrieved_work.word_count == new_work.word_count
        assert retrieved_work.submission_date == new_work.submission_date
        assert retrieved_work.last_update_date == new_work.last_update_date
        assert retrieved_work.archive_date == new_work.archive_date
        # relationship assertions
        assert retrieved_work.critiques == [new_critique_1, new_critique_2]
        assert retrieved_work.member_id == new_member.id

    @pytest.mark.skip(reason="Throwaway test file for testing ORM functionality")
    def test_create_and_retrieve_critique(self, session, valid_critique, valid_work, valid_rating):
        # Arrange
        new_critique = valid_critique
        new_critique.work_id = valid_work.id

        new_rating = valid_rating
        new_rating._critique_id = new_critique.id

        valid_critique.add_rating(new_rating)

        # Act
        session.add(new_critique)
        session.commit()
        retrieved_critique = session.query(Critique).filter_by(content_about="About content.").one()

        # Assert
        assert retrieved_critique.id == new_critique.id
        assert retrieved_critique.content_about == "About content."
        assert retrieved_critique.content_about == "About content."
        assert retrieved_critique.content_successes == "This is a test critique."
        assert retrieved_critique.content_weaknesses == "This is a test critique."
        assert retrieved_critique.content_ideas == "This is a test critique."
        assert retrieved_critique.work_id == valid_work.id
        assert retrieved_critique.ratings == [new_rating]

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
