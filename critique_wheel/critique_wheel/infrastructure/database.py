import logging

import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

from critique_wheel import config

logger = logging.getLogger(__name__)


# DB configuration
def get_postgres_uri():
    logger.debug(f"ENV_STATE is {config.BaseConfig().ENV_STATE}")
    host = config.config.DB_HOST
    port = 54321 if host == "localhost" else 5432
    password = config.config.DB_PASSWORD
    user = config.config.DB_USER
    db_name = config.config.DB_NAME
    logger.debug(f"Using {db_name}")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_engine():
    logger.debug("Creating database engine...")
    engine = sqlalchemy.create_engine(
        get_postgres_uri(),
        # connect_args={"check_same_thread": False},
    )
    logger.debug(f"Database {get_postgres_uri()} created.")
    return engine


def get_session_local():
    logger.debug("Creating database session...")
    logger.debug(f"Using {config.BaseConfig().ENV_STATE} state")
    SessionLocal = sqlalchemy.orm.sessionmaker(
        autocommit=False, autoflush=False, bind=get_engine()
    )

    return SessionLocal
