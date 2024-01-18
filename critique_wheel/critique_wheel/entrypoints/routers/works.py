import logging

import fastapi
import fastapi.exception_handlers
from sqlalchemy.orm import Session

from critique_wheel.entrypoints.schemas import schemas
from critique_wheel.infrastructure import database as db_config
from critique_wheel.works.services import unit_of_work, work_service

logger = logging.getLogger(__name__)

router = fastapi.APIRouter()


async def get_db_session():
    db = db_config.get_postgres_session_local()
    yield db


@router.post("/work")
async def create_work(
    work: schemas.UserWorkIn,
    session_factory: Session = fastapi.Depends(get_db_session),
):
    logger.debug("Creating work.")
    result = work_service.add_work(
        uow=unit_of_work.WorkUnitOfWork(session_factory=session_factory),
        title=work.title,
        content=work.content,
        member_id=work.member_id,
        genre=work.genre,
        age_restriction=work.age_restriction,
    )
    return result


@router.get("/work/{work_id}")
async def get_work_by_id(work_id: str):
    work = work_service.get_work_by_id(
        work_id=work_id, uow=unit_of_work.WorkUnitOfWork()
    )
    if not work:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Work with id {work_id} not found"
        )
    return work
