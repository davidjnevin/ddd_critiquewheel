import logging

import fastapi
import fastapi.exception_handlers
from asgi_correlation_id import CorrelationIdMiddleware

from critique_wheel.adapters import orm
from critique_wheel.api.routers import healthcheck, works
from critique_wheel.logging_conf import configure_logging

configure_logging()
logger = logging.getLogger(__name__)
logger.debug(f"Starting {__name__}...")


app = fastapi.FastAPI(
    title="Critique Wheel API", version="0.0.1", openapi_url="/openapi.json"
)
app.add_middleware(CorrelationIdMiddleware)

app.include_router(healthcheck.router)
app.include_router(works.router)


@app.exception_handler(fastapi.HTTPException)
async def http_exception_handle_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code}  {exc.detail}")
    return await fastapi.exception_handlers.http_exception_handler(request, exc)


if __name__ == "__main__":
    import uvicorn

    logger.debug("Creating database engine...")
    orm.MapperRegistry.start_mappers()

    uvicorn.run(app)
