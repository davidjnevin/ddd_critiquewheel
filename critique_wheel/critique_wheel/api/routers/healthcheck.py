import fastapi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from critique_wheel.infrastructure.config import config as infr_config

router = fastapi.APIRouter()


def get_db_session():
    get_session = sessionmaker(bind=create_engine(infr_config.get_postgres_uri()))
    return get_session()


@router.get("/healthcheck")
async def healthcheck(session=fastapi.Depends(get_db_session)):
    return {"status": "ok"}
