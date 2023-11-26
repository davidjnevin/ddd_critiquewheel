from sqlalchemy import text

from critique_wheel.adapters.sqlalchemy import credit_repository


def test_repository_can_save_a_critique_credit_transaction(
    session, valid_credit, valid_member, valid_critique
):
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

    rows = list(
        session.execute(
            text(
                'SELECT id, member_id, amount, transaction_type, work_id, critique_id FROM "credits"'
            )
        )
    )
    assert rows == [
        (
            credit.id.get_uuid(),
            member.id.get_uuid(),
            credit.amount,
            credit.transaction_type.value,
            None,
            critique.id.get_uuid(),
        )
    ]


def test_repository_can_save_a_work_credit_transaction(
    session, valid_credit, valid_member, valid_work
):
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

    rows = list(
        session.execute(
            text(
                'SELECT id, member_id, amount, transaction_type, work_id, critique_id FROM "credits"'
            )
        )
    )
    assert rows == [
        (
            credit.id.get_uuid(),
            member.id.get_uuid(),
            credit.amount,
            credit.transaction_type.value,
            work.id.get_uuid(),
            None,
        )
    ]
