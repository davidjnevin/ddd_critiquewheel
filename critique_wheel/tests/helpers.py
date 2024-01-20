import logging
import uuid

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from critique_wheel.adapters.orm import mapper_registry

logger = logging.getLogger(__name__)


# Possibly can be moved to a fixture
def override_get_db_session():
    SQLITE_DB_URI = "sqlite:///"
    engine = create_engine(
        SQLITE_DB_URI,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        # echo=True,
    )
    logger.debug(f"Using {engine} database engine")
    mapper_registry.metadata.create_all(engine)
    try:
        db = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
        )
        yield db
    finally:
        db().close()


def insert_member(session, **kwargs):
    stmt = sqlalchemy.text(
        """
        INSERT INTO members (id, username, email, password)
        VALUES (:id, :username, :email, :password)
        """
    )
    params = kwargs
    session.execute(stmt, params)


def get_member_by_id(session, member_id):
    stmt = sqlalchemy.text(
        """
        SELECT id, username, email, password
        FROM members
        WHERE id = :id
        """
    )
    params = {
        "id": member_id,
    }
    result = session.execute(stmt, params)
    row = result.fetchone()
    if row:
        return row._mapping
    else:
        return None


def create_and_insert_member(session):
    id = str(uuid.uuid4())
    member = {
        "id": id,
        "username": "Peter Pan",
        "password": "adsfhjsdaf65rtdTTFd!",
        "email": "some_random+password@davidnevin.net",
    }
    insert_member(session, **member)
    return id
