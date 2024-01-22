import logging

import fastapi
import fastapi.exception_handlers
from sqlalchemy.orm import Session

from critique_wheel.entrypoints.schemas import schemas
from critique_wheel.infrastructure import database as db_config
from critique_wheel.members.services import iam_service, unit_of_work

logger = logging.getLogger(__name__)

router = fastapi.APIRouter(
    prefix="/members",
)


def get_db_session():
    db: Session = db_config.get_postgres_session_local()
    yield db


@router.post(
    "/",
    response_model=schemas.UserMember,
    status_code=201,
)
def create_member(
    member: schemas.UserMemberIn,
    db: Session = fastapi.Depends(get_db_session),
):
    logger.debug("Creating member.")
    result = iam_service.add_member(
        uow=unit_of_work.IAMUnitOfWork(session_factory=db),
        username=member.username,
        email=member.email,
        password=member.password,
    )
    return result


@router.post(
    "/register",
    response_model=schemas.RegisterMemberSuccess,
    status_code=201,
)
def register_member(
    member: schemas.RegisterMemberIn,
    db: Session = fastapi.Depends(get_db_session),
):
    logger.debug("Registering member.")
    iam_service.register_member(
        uow=unit_of_work.IAMUnitOfWork(session_factory=db),
        username=member.username,
        email=member.email,
        password=member.password,
        confirm_password=member.confirm_password,
    )
    return {
        "detail": "User created. Please confirm your email",
    }
