import logging

import fastapi
import fastapi.exception_handlers
from sqlalchemy.orm import Session

from critique_wheel.entrypoints.schemas import schemas
from critique_wheel.infrastructure import database as db_config
from critique_wheel.members.services import iam_service, unit_of_work

logger = logging.getLogger(__name__)

router = fastapi.APIRouter()


def get_db_session():
    db: Session = db_config.get_session_local()
    yield db


@router.post("/member", response_model=schemas.UserMemberOut, status_code=201)
def create_member(
    member: schemas.UserMemberIn, db: Session = fastapi.Depends(get_db_session)
):
    logger.debug("Creating member.")
    result = iam_service.add_member(
        uow=unit_of_work.IAMUnitOfWork(),
        username=member.username,
        email=member.email,
        password=member.password,
    )
    return result
