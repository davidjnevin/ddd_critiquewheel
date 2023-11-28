import fastapi
import fastapi.exception_handlers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from critique_wheel.adapters.sqlalchemy import work_repository
from critique_wheel.api.schemas.work_schemas import (
    WorkPayloadSchema,
    WorkResponseSchema,
)
from critique_wheel.infrastructure.config import config as infr_config
from critique_wheel.works.services.work_service import WorkService

router = fastapi.APIRouter()


def get_db_session():
    get_session = sessionmaker(bind=create_engine(infr_config.get_postgres_uri()))
    return get_session()


@router.get("/works")
def list_works(session=fastapi.Depends(get_db_session)):
    repo = work_repository.SqlAlchemyWorkRepository(session)
    service = WorkService(repo)
    return service.list_works()


@router.post("/works", response_model=WorkResponseSchema, status_code=201)
def create_work(payload: WorkPayloadSchema):
    pass
