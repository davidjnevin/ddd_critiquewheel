import uuid

from critique_wheel.infrastructure.config import config


def format_uuid_for_db(uuid_str):
    if config.TESTING_USING_SQLITE:
        return str(uuid_str).replace("-", "")
    else:
        # Default behavior for other databases
        return str(uuid.UUID(str(uuid_str)))
