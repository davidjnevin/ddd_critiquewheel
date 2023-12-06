import logging

import fastapi

logger = logging.getLogger(__name__)

router = fastapi.APIRouter()


@router.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
