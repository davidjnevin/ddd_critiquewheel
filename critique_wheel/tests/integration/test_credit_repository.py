from sqlalchemy import text

from critique_wheel.adapters.sqlalchemy import credit_repository
from critique_wheel.infrastructure.utils.db_utils import format_uuid_for_db


def test_repository_can_save_a_critique_credit_transaction(session, valid_credit, valid_member,  valid_critique):
    credit = valid_credit
    member = valid_member
    critique = valid_critique

    # Assign all to one member
    credit.member_id = member.id
    critique.member_id = member.id
    credit.work_id = None
    credit.critique_id = critique.id

    repo = credit_repository.SqlAlchemyCreditRepository(session)
    repo.add(credit)
    session.commit()

    rows = list(session.execute(text(
        'SELECT id, member_id, amount, transaction_type, work_id, critique_id FROM "credits"'
    )))
    assert rows == [
        (
            format_uuid_for_db(credit.id),
            format_uuid_for_db(member.id),
            credit.amount,
            credit.transaction_type.value,
            None,
            format_uuid_for_db(critique.id),
        )
    ]


def test_repository_can_save_a_work_credit_transaction(session, valid_credit, valid_member, valid_work):
    credit = valid_credit
    member = valid_member
    work = valid_work

    # Assign all to one member
    credit.member_id = member.id
    work.member_id = member.id
    credit.critique_id = None
    credit.work_id = work.id

    repo = credit_repository.SqlAlchemyCreditRepository(session)
    repo.add(credit)
    session.commit()

    rows = list(session.execute(text(
        'SELECT id, member_id, amount, transaction_type, work_id, critique_id FROM "credits"'
    )))
    assert rows == [
        (
            format_uuid_for_db(credit.id),
            format_uuid_for_db(member.id),
            credit.amount,
            credit.transaction_type.value,
            format_uuid_for_db(work.id),
            None,
        )
    ]

