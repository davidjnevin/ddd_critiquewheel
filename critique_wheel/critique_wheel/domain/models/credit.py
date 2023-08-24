import os
from datetime import datetime
from enum import Enum
from uuid import uuid4

import yaml
from dotenv import load_dotenv

load_dotenv()

CREDIT_RULES_FILE_PATH = os.getenv("CREDIT_RULES_FILE_PATH")

assert os.path.exists(CREDIT_RULES_FILE_PATH), f"File not found at {CREDIT_RULES_FILE_PATH}"  # type: ignore


class TransactionType(str, Enum):
    CRITIQUE_GIVEN = "critique_given"
    WORK_SUBMITTED = "work_submitted"
    NEW_MEMBER_BONUS = "new_member_bonus"
    PROFILE_COMPLETEION_BONUS = "profile_completion_bonus"

# Mock database to facilitate testing and building domain logic without a database
mock_db = {
    "transactions": []
}

class CreditTransaction:
    CREDIT_RULES = {}

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
    def load_credit_rules_from_yaml(cls, filepath=CREDIT_RULES_FILE_PATH):
        with open(filepath, "r") as file:  # type: ignore
            credit_settings = yaml.safe_load(file)
        cls.validate_credit_rules(credit_settings.get("rules", {}))
        cls.CREDIT_RULES = credit_settings.get("rules", {})

    @classmethod
    def validate_credit_rules(cls, credit_rules):
        # Check if main keys 'submission' and 'critique' exist
        if not all(key in credit_rules for key in ['submission', 'critique']):
            raise ValueError("YAML file must contain 'submission' and 'critique' rules.")

        # Validate 'submission' and 'critique' rules
        for rule_type in ['submission', 'critique']:
            if not isinstance(credit_rules[rule_type], list):
                raise ValueError(f"'{rule_type}' must be a list of rules.")

            for rule in credit_rules[rule_type]:
                if not all(key in rule for key in ['max_words', 'credits']):
                    raise ValueError(f"Each rule in '{rule_type}' must contain 'max_words' and 'credits'.")

                if not (isinstance(rule['max_words'], int) or rule['max_words'] == 'max'):
                    raise ValueError(f"'max_words' in '{rule_type}' must be an integer or 'max'.")

                if not isinstance(rule['credits'], (int, float)):
                    raise ValueError(f"'credits' in '{rule_type}' must be a number.")


    @classmethod
    def create(
        cls,
        member_id,
        amount,
        transaction_type,
        work_id=None,
        critique_id=None,
        transaction_id=None,
        date=None,
    ):
        # Validate the transaction_type and the associated work_id and critique_id
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

