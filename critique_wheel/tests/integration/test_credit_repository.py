from sqlalchemy import text

from critique_wheel.adapters.sqlalchemy import credit_repository
from critique_wheel.infrastructure.utils.db_utils import format_uuid_for_db


def test_repository_can_save_a_credit_transaction(session, valid_credit):
    credit = valid_credit
    repo = credit_repository.SqlAlchemyCreditRepository(session)
    repo.add(credit)
    session.commit()

    rows = list(session.execute(text(
        'SELECT id, member_id, amount, transaction_type, work_id, critique_id FROM "credits"'
    )))
    assert rows == [
        (
            format_uuid_for_db(credit.id),
            format_uuid_for_db(credit.member_id),
            credit.amount,
            credit.transaction_type.value,
            format_uuid_for_db(credit.work_id),
            format_uuid_for_db(credit.critique_id),
        )
    ]


def test_repository_can_get_a_credit_transaction_by_id(session, valid_credit):
    credit = valid_credit
    repo = credit_repository.SqlAlchemyCreditRepository(session)
    repo.add(credit)
    session.commit()

    id_to_get = credit.id
    stmt = text('SELECT id, member_id, amount, transaction_type, work_id, critique_id FROM "credits" WHERE id=:id').bindparams(
        id=id_to_get
    )
    rows = session.execute(stmt).fetchall()
    assert rows == [
        (
            format_uuid_for_db(credit.id),
            format_uuid_for_db(credit.member_id),
            credit.amount,
            credit.transaction_type.value,
            format_uuid_for_db(credit.work_id),
            format_uuid_for_db(credit.critique_id),
        )
    ]
