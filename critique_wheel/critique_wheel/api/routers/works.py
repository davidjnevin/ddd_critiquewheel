import fastapi
import fastapi.exception_handlers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from critique_wheel.api.schemas.work_schemas import (
    WorkPayloadSchema,
    WorkResponseSchema,
)
from critique_wheel.infrastructure.config import config

router = fastapi.APIRouter()


def get_db_session():
    get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
    return get_session()


@router.post("/works", response_model=WorkResponseSchema, status_code=201)
def create_work(payload: WorkPayloadSchema):
    pass
