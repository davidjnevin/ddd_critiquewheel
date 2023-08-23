from datetime import datetime
from enum import Enum
from uuid import uuid4


class TransactionType(str, Enum):
    CRITIQUE_GIVEN = "critique_given"
    WORK_SUBMITTED = "work_submitted"
    NEW_MEMBER_BONUS = "new_member_bonus"
    PROFILE_COMPLETEION_BONUS = "profile_completion_bonus"


class CreditTransaction:
    def __init__(
        self,
        member_id,
        amount,
        work_id=None,
        critique_id=None,
        transaction_type=TransactionType.CRITIQUE_GIVEN,
        transaction_id=None,
        date=None,
    ):
        self.id = transaction_id or uuid4()
        self.member_id = member_id
        self.critique_id = critique_id
        self.work_id = work_id
        self.amount = amount
        self.date_of_transaction = date or datetime.now()
        self.transaction_type = transaction_type

    @classmethod
    def create(
        cls,
        member_id,
        amount,
        transaction_type=TransactionType.CRITIQUE_GIVEN,
        work_id=None,
        critique_id=None,
        transaction_id=None,
        date=None,
    ):
        if transaction_type == TransactionType.WORK_SUBMITTED and (work_id is None or critique_id is not None):
            raise ValueError("Work submission must only have an associated work_id.")
        if transaction_type == TransactionType.CRITIQUE_GIVEN and (critique_id is None or work_id is None):
            raise ValueError("Critique submission must have an associated critique_id and work_id.")
        return cls(
            member_id=member_id,
            work_id=work_id,
            critique_id=critique_id,
            amount=amount,
            transaction_type=transaction_type,
            transaction_id=transaction_id,
            date=date,
        )
