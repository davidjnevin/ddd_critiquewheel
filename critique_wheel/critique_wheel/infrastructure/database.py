import logging

import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

from critique_wheel import config

logger = logging.getLogger(__name__)


def get_engine():
    logger.debug(f"Using {config.BaseConfig().ENV_STATE}")
    logger.debug("Creating database engine...")
    engine = sqlalchemy.create_engine(
        config.get_postgres_uri(),
        # connect_args={"check_same_thread": False},
    )
    logger.debug(f"Database {config.get_postgres_uri()} created.")
    return engine


def get_session_local():
    logger.debug(f"Using {config.BaseConfig().ENV_STATE}")
    logger.debug("Creating database session...")
    SessionLocal = sqlalchemy.orm.sessionmaker(
        autocommit=False, autoflush=False, bind=get_engine()
    )

    return SessionLocal
