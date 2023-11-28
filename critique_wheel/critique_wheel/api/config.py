import logging
from functools import lru_cache

from pydantic import AnyUrl
from pydantic_settings import BaseSettings

from critique_wheel.config import config

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    environment: str = config.ENV_STATE
    testing: bool = bool(0)
    database_url: AnyUrl = None


@lru_cache
def get_settings() -> BaseSettings:
    logger.info("Loading config settings from the environment.")
    return Settings()
