from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from critique_wheel.adapters import orm
from critique_wheel.api.ping import router as ping_router
from critique_wheel.infrastructure.config import config

app = FastAPI(title="Critique Wheel API", openapi_url="/openapi.json")


def get_db_session():
    get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
    return get_session()


app.include_router(ping_router)

if __name__ == "__main__":
    import uvicorn

    orm.start_mappers()
    uvicorn.run(app, host="localhost", port=8000)
