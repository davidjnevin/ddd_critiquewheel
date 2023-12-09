import logging

import fastapi
import fastapi.exception_handlers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from critique_wheel.adapters.sqlalchemy.work_repository import WorkRepository
from critique_wheel.api.schemas.schemas import UserWork, UserWorkIn
from critique_wheel.config import get_postgres_uri
from critique_wheel.works.services import work_service

logger = logging.getLogger(__name__)

router = fastapi.APIRouter()


def get_db_session():
    get_session = sessionmaker(bind=create_engine(get_postgres_uri()))
    return get_session()


@router.post("/work", response_model=UserWork, status_code=201)
async def create_work(work: UserWorkIn, session=fastapi.Depends(get_db_session)):
    repo = WorkRepository(session)
    logger.info("Creating work.")

    try:
        work = work_service.add_work(repo, session, **work.model_dump())
    except Exception as e:
        logger.error(f"Error creating work: {e}")
        raise fastapi.HTTPException(
            status_code=500, detail="Error creating work. Please try again later."
        )
    return work


@router.get("/work/{work_id}")
async def get_work_by_id(work_id: str, session=fastapi.Depends(get_db_session)):
    repo = WorkRepository(session)
    logger.info(f"Getting work: {work_id}")
    work = work_service.get_work_by_id(work_id, repo)
    if not work:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Work with id {work_id} not found"
        )
    return work
