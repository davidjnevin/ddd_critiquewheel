from datetime import datetime

import pytest

from critique_wheel.domain.models.credit import CreditTransaction, TransactionType


@pytest.mark.current
class TestTransactionType:
    def test_can_generate_credit_transation(self):
        ct = CreditTransaction(
            member_id=42,
            work_id=45,
            critique_id=46,
            amount=3,
            transaction_id=23,
            date=datetime.now(),
        )
        assert ct.id == 23
        assert ct.member_id == 42
        assert ct.critique_id == 46
        assert ct.work_id == 45
        assert ct.amount == 3
        assert ct.transaction_type == TransactionType.CRITIQUE_GIVEN
        assert ct.date_of_transaction.date() == datetime.now().date()

    def test_create_transaction(self):
        ct = CreditTransaction.create(
            member_id=42,
            work_id=45,
            critique_id=None,
            amount=3,
            transaction_id=23,
            transaction_type=TransactionType.WORK_SUBMITTED,
            date=datetime.now(),
        )
        assert ct.id == 23
        assert ct.member_id == 42
        assert ct.critique_id == None
        assert ct.work_id == 45
        assert ct.amount == 3
        assert ct.transaction_type == TransactionType.WORK_SUBMITTED
        assert ct.date_of_transaction.date() == datetime.now().date()

    def test_critique_given_credit_transaction_with_critique_id_and_work_id(self):
        member_id = 45
        amount = 3
        work_id = 45
        transaction_type = TransactionType.CRITIQUE_GIVEN
        critique_id = 46

        ct = CreditTransaction.create(
            member_id=member_id,
            amount=amount,
            transaction_type=transaction_type,
            critique_id=critique_id,
            work_id=work_id,
        )
        assert ct.critique_id == critique_id
        assert ct.work_id == work_id
        assert ct.transaction_type == TransactionType.CRITIQUE_GIVEN

    def test_critique_given_credit_transaction_without_work_id(self):
        member_id = 43
        amount = 3
        work_id = None  # deliberately set to None
        critique_id = 46
        transaction_type = TransactionType.CRITIQUE_GIVEN

        with pytest.raises(
            ValueError,
            match="Critique submission must have an associated critique_id and work_id.",
        ):
            CreditTransaction.create(
                member_id=member_id,
                amount=amount,
                transaction_type=transaction_type,
                work_id=work_id,
                critique_id=critique_id,
                transaction_id=None,
                date=None,
            )

    def test_critique_given_credit_transaction_without_critique_id(self):
        member_id = 43
        amount = 3
        work_id = 45
        critique_id = None  # deliberately set to None
        transaction_type = TransactionType.CRITIQUE_GIVEN

        with pytest.raises(
            ValueError,
            match="Critique submission must have an associated critique_id",
        ):
            CreditTransaction.create(
                member_id=member_id,
                amount=amount,
                transaction_type=transaction_type,
                work_id=work_id,
                critique_id=critique_id,
                transaction_id=None,
                date=None,
            )

    def test_work_submitted_credit_transaction_with_work_id_and_with_critique_id(self):
        member_id = 45
        amount = 3
        transaction_type = TransactionType.CRITIQUE_GIVEN
        work_id = 45
        critique_id = 46

        ct = CreditTransaction.create(
            member_id=member_id,
            amount=amount,
            transaction_type=transaction_type,
            work_id=work_id,
            critique_id=critique_id,
        )
        assert ct.work_id == 45

    def test_work_submission_credit_transaction_without_work_id(self):
        member_id = 43
        amount = 3
        transaction_type = TransactionType.WORK_SUBMITTED

        with pytest.raises(ValueError, match="Work submission must only have an associated work_id."):
            CreditTransaction.create(
                member_id=member_id,
                amount=amount,
                transaction_type=transaction_type,
                work_id=None,
                critique_id=None,
                transaction_id=None,
                date=None,
            )

    def test_work_submission_credit_transaction_with_work_id_and_critique_id(self):
        member_id = 43
        amount = 3
        work_id = 45
        critique_id = 46
        transaction_type = TransactionType.WORK_SUBMITTED

        with pytest.raises(ValueError, match="Work submission must only have an associated work_id"):
            CreditTransaction.create(
                member_id=member_id,
                amount=amount,
                transaction_type=transaction_type,
                work_id=work_id,
                critique_id=critique_id,
                transaction_id=None,
                date=None,
            )
