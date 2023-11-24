from sqlalchemy import text
import pytest
from critique_wheel.adapters.sqlalchemy import rating_repository
from critique_wheel.infrastructure.utils.db_utils import format_uuid_for_db

def test_repository_can_save_a_rating(session, valid_rating):
    rating = valid_rating
    repo = rating_repository.SqlAlchemyRatingRepository(session)
    repo.add(rating)
    session.commit()

    rows = list(session.execute(text('SELECT id, score, comment, member_id, critique_id, status FROM "ratings"')))
    assert rows == [
        (
            format_uuid_for_db(rating.id),
            rating.score,
            rating.comment,
            rating.member_id.get_uuid(),
            format_uuid_for_db(rating.critique_id),
            rating.status.value,
        )
    ]

def test_repo_can_list_and_get_ratings(session, valid_rating):
    rating = valid_rating
    repo = rating_repository.SqlAlchemyRatingRepository(session)
    repo.add(rating)
    session.commit()
    assert repo.get(rating.id) == rating
    assert repo.list() == [rating]

def test_repository_can_get_a_work_by_id(session, valid_rating):
    rating = valid_rating
    repo = rating_repository.SqlAlchemyRatingRepository(session)
    repo.add(rating)
    session.commit()

    id_to_get = rating.id
    stmt = text(
        'SELECT id, score, comment, critique_id, member_id, status FROM "ratings" WHERE id=:id_to_get'
    ).bindparams(id_to_get=id_to_get)

    rows = session.execute(stmt).fetchall()
    assert rows == [
        (
            format_uuid_for_db(rating.id),
            rating.score,
            rating.comment,
            format_uuid_for_db(rating.critique_id),
            rating.member_id.get_uuid(),
            rating.status.value,
        )
    ]
