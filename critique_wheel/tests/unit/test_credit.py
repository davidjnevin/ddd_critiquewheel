from datetime import datetime

import pytest

from critique_wheel.domain.models.credit import CreditManager, TransactionType

# Mock database setup
mock_db = {
    "transactions": [],
}


# Reset the mock database before each test
@pytest.fixture(autouse=True)
def reset_mock_db():
    mock_db["transactions"].clear()


@pytest.mark.current
class TestTransactionType:
    def test_setup(self):
        assert TransactionType.CRITIQUE_GIVEN == "critique_given"
        assert TransactionType.WORK_SUBMITTED == "work_submitted"
        assert TransactionType.NEW_MEMBER_BONUS == "new_member_bonus"
        assert TransactionType.PROFILE_COMPLETEION_BONUS == "profile_completion_bonus"

    def test_can_generate_credit_transation(self):
        ct = CreditManager(
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
        ct = CreditManager.create(
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

        ct = CreditManager.create(
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
            CreditManager.create(
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
            CreditManager.create(
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

        ct = CreditManager.create(
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
            CreditManager.create(
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

        with pytest.raises(
            ValueError,
            match="Work submission must only have an associated work_id",
        ):
            CreditManager.create(
                member_id=member_id,
                amount=amount,
                transaction_type=transaction_type,
                work_id=work_id,
                critique_id=critique_id,
                transaction_id=None,
                date=None,
            )

    def test_load_credit_rules_from_yaml(self, tmp_path):
        # Create a temporary YAML file with credit rules
        credit_rules_content = """
        rules:
          submission:
            - max_words: 3000
              credits: 3
            - max_words: 4000
              credits: 3
            - max_words: 5000
              credits: 4
            - max_words: max
              credits: 5
          critique:
            - max_words: 3000
              credits: 1
            - max_words: 4000
              credits: 1.5
            - max_words: 5000
              credits: 2
            - max_words: max
              credits: 2.5
          bonus:
            new_user: 2
        """
        credit_rules_file = tmp_path / "credit_rules.yaml"
        credit_rules_file.write_text(credit_rules_content)

        # Load the credit rules from the temporary YAML file
        CreditManager.load_credit_rules_from_yaml(filepath=credit_rules_file)

        # Assert that the credit rules are loaded correctly
        assert CreditManager.CREDIT_RULES["submission"][0]["max_words"] == 3000
        assert CreditManager.CREDIT_RULES["submission"][0]["credits"] == 3
        assert CreditManager.CREDIT_RULES["critique"][1]["max_words"] == 4000
        assert CreditManager.CREDIT_RULES["critique"][1]["credits"] == 1.5
        assert CreditManager.CREDIT_RULES["bonus"]["new_user"] == 2

    def test_load_credit_rules_from_yaml_with_invalid_yaml(self):
        # Valid credit rules
        valid_rules = {
            "submission": [
                {"max_words": 3000, "credits": 3},
                {"max_words": 4000, "credits": 3},
                {"max_words": "max", "credits": 5},
            ],
            "critique": [
                {"max_words": 3000, "credits": 1},
                {"max_words": 4000, "credits": 1.5},
                {"max_words": "max", "credits": 2.5},
            ],
        }

        # No exception should be raised for valid rules
        CreditManager.validate_credit_rules(valid_rules)

        # Missing 'submission' key
        with pytest.raises(
            ValueError,
            match="YAML file must contain 'submission' and 'critique' rules.",
        ):
            CreditManager.validate_credit_rules({"critique": valid_rules["critique"]})

        # Missing 'critique' key
        with pytest.raises(ValueError, match="YAML file must contain 'submission' and 'critique' rules."):
            CreditManager.validate_credit_rules({"submission": valid_rules["submission"]})

        # 'submission' is not a list
        with pytest.raises(ValueError, match="'submission' must be a list of rules."):
            CreditManager.validate_credit_rules({"submission": {}, "critique": valid_rules["critique"]})

        # Missing 'max_words' in a rule
        with pytest.raises(ValueError, match="Each rule in 'submission' must contain 'max_words' and 'credits'."):
            CreditManager.validate_credit_rules(
                {"submission": [{"credits": 3}], "critique": valid_rules["critique"]}
            )

        # 'max_words' is neither integer nor 'max'
        with pytest.raises(ValueError, match="'max_words' in 'submission' must be an integer or 'max'."):
            CreditManager.validate_credit_rules(
                {"submission": [{"max_words": "three thousand", "credits": 3}], "critique": valid_rules["critique"]}
            )

        # 'credits' is not a number
        with pytest.raises(ValueError, match="'credits' in 'submission' must be a number."):
            CreditManager.validate_credit_rules(
                {"submission": [{"max_words": 3000, "credits": "three"}], "critique": valid_rules["critique"]}
            )


    def test_credits_for_submission(self):
        assert CreditManager.credits_for_submission(2500) == 3
        assert CreditManager.credits_for_submission(3500) == 3
        assert CreditManager.credits_for_submission(4500) == 4
        assert CreditManager.credits_for_submission(6000) == 5

    def test_credits_for_critique(self):
        assert CreditManager.credits_for_critique(2500) == 1
        assert CreditManager.credits_for_critique(3500) == 1.5
        assert CreditManager.credits_for_critique(4500) == 2
        assert CreditManager.credits_for_critique(6000) == 2.5

