import logging

import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

from critique_wheel import config
from critique_wheel.adapters.orm import mapper_registry

logger = logging.getLogger(__name__)


# Postgres DB configuration
def get_postgres_uri():
    logger.debug(f"ENV_STATE is {config.BaseConfig().ENV_STATE}")
    host = config.config.DB_HOST
    port = 54321 if host == "localhost" else 5432
    password = config.config.DB_PASSWORD
    user = config.config.DB_USER
    db_name = config.config.DB_NAME
    logger.debug(f"DB_NAME is {db_name}")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


# Sqlite DB configuration
def get_sqlite_uri():
    logger.debug(f"ENV_STATE is {config.BaseConfig().ENV_STATE}")
    logger.debug("Using sqlite in memory database")
    return "sqlite:///:memory:"


def get_postgres_engine():
    logger.debug(f"Using {config.BaseConfig().ENV_STATE} state")
    logger.debug("Creating database engine...")
    engine = sqlalchemy.create_engine(
        get_postgres_uri(),
    )
    mapper_registry.metadata.create_all(engine)
    logger.debug(f"Database {get_postgres_uri()} created.")
    return engine


def get_sqlite_engine():
    logger.debug(f"Using {config.BaseConfig().ENV_STATE} state")
    logger.debug("Creating database engine...")
    engine = sqlalchemy.create_engine(
        get_sqlite_uri(),
        connect_args={"check_same_thread": False},
        # echo=True,
    )
    mapper_registry.metadata.create_all(engine)
    logger.debug(f"Engine {engine} created.")
    return engine


def get_sqlite_session():
    logger.debug(f"Using {config.BaseConfig().ENV_STATE} state")
    logger.debug("Creating sqlite database sessionfactory...")
    LocalSessionMaker = sqlalchemy.orm.sessionmaker(
        # autocommit=False,
        # autoflush=False,
        bind=get_sqlite_engine(),
    )

    return LocalSessionMaker


def get_postgres_session_local():
    logger.debug(f"Using {config.BaseConfig().ENV_STATE} state")
    logger.debug("Creating postgres database sessionfactory...")
    LocalSessionMaker = sqlalchemy.orm.sessionmaker(
        # autocommit=False,
        # autoflush=False,
        bind=get_postgres_engine(),
    )

    return LocalSessionMaker
