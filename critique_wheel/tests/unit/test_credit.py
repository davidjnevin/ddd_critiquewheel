from datetime import datetime

import pytest

from critique_wheel.domain.models.credit import CreditTransaction, TransactionType


def test_can_generate_credit_transation():
    ct = CreditTransaction(
        member_id=42,
        work_id=45,
        amount=3,
        transaction_id=23,
        date=datetime.now(),
    )
    assert ct.id == 23
    assert ct.member_id == 42
    assert ct.work_id == 45
    assert ct.amount == 3
    assert ct.transaction_type == TransactionType.CRITIQUE_GIVEN
    assert ct.date_of_transaction.date() == datetime.now().date()

def test_create_transaction():
    ct = CreditTransaction.create(
        member_id=42,
        work_id=45,
        amount=3,
        transaction_id=23,
        transaction_type=TransactionType.WORK_SUBMITTED,
        date=datetime.now(),
    )
    assert ct.id == 23
    assert ct.member_id == 42
    assert ct.work_id == 45
    assert ct.amount == 3
    assert ct.transaction_type == TransactionType.WORK_SUBMITTED
    assert ct.date_of_transaction.date() == datetime.now().date()


