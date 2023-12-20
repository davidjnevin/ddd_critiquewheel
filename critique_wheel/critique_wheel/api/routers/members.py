import logging

import fastapi
import fastapi.exception_handlers
from sqlalchemy.orm import Session

from critique_wheel.api.schemas import schemas
from critique_wheel.infrastructure import database as db_config
from critique_wheel.members.services import member_service, unit_of_work

logger = logging.getLogger(__name__)

router = fastapi.APIRouter()


async def get_db_session():
    db = db_config.get_session_local()
    try:
        yield db
    finally:
        db.close


@router.post("/member")
async def create_member(
    member: schemas.UserMemberIn,
    session_factory: Session = fastapi.Depends(get_db_session),
):
    logger.debug("Creating member.")
    result = member_service.add_member(
        uow=unit_of_work.MemberUnitOfWork(session_factory),
        username=member.title,
        email=member.email,
        password=member.password,
    )
    return result
