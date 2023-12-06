import logging

import fastapi
import fastapi.exception_handlers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from critique_wheel.adapters.sqlalchemy.work_repository import SqlAlchemyWorkRepository
from critique_wheel.config import get_postgres_uri
from critique_wheel.works.services import work_service
from critique_wheel.works.value_objects import WorkId

logger = logging.getLogger(__name__)

router = fastapi.APIRouter()


def get_db_session():
    get_session = sessionmaker(bind=create_engine(get_postgres_uri()))
    return get_session()


@router.get("/works/{work_id}")
async def get_work_by_id(work_id: str):
    session = get_db_session()
    repo = SqlAlchemyWorkRepository(session)
    logger.info(f"Getting work {work_id}.")
    work = work_service.get_work_by_id(WorkId.from_string(work_id), repo)
    if not work:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Work with id {work_id} not found"
        )
    return work
