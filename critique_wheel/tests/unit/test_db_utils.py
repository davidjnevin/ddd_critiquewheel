from critique_wheel.infrastructure.config import config
from critique_wheel.infrastructure.utils import db_utils


def test_format_uuid_based_on_feature_flag():
    # Given
    config.TESTING_USING_SQLITE = True
    test_uuid = "123e4567-e89b-12d3-a456-426614174000"
    assert db_utils.format_uuid_for_db(test_uuid) == "123e4567e89b12d3a456426614174000"

    config.TESTING_USING_SQLITE = False
    test_uuid = "123e4567-e89b-12d3-a456-426614174000"
    assert (
        db_utils.format_uuid_for_db(test_uuid) == "123e4567-e89b-12d3-a456-426614174000"
    )
