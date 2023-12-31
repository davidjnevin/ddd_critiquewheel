import logging
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )


class GlobalConfig(BaseConfig):
    # Work configuration
    WORK_MAX_WORDS: Optional[int] = 8000
    CRITIQUE_ABOUT_MIN_WORDS: Optional[int] = 20
    CRITIQUE_SUCCESSES_MIN_WORDS: Optional[int] = 40
    CRITIQUE_WEAKNESSES_MIN_WORDS: Optional[int] = 40
    CRITIQUE_IDEAS_MIN_WORDS: Optional[int] = 40
    LOG_FILE: Optional[str] = None
    LOGTAIL_API_KEY: Optional[str] = None
    FORCE_ROLLBACK: Optional[bool] = False
    DB_HOST: Optional[str] = "localhost"
    DB_PASSWORD: Optional[str] = "abc123"
    DB_USER: Optional[str] = "abc123"
    DB_NAME: Optional[str] = "abc123"
    API_HOST: Optional[str] = "localhost"
    # JWT_ALGORITHM: Optional[str] = None
    # JWT_SECRET_KEY: Optional[str] = None
    # MAILGUN_API_KEY: Optional[str] = None
    # MAILGUN_DOMAIN: Optional[str] = None
    # B2_API_KEY_ID: Optional[str] = None
    # B2_BUCKET_NAME: Optional[str] = None
    # B2_API_KEY: Optional[str] = None
    # OPENAI_API_KEY: Optional[str] = None
    # OPENAI_IMAGE_SIZE: Optional[str] = None
    # SENTRY_DSN: Optional[str] = None


class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_")


class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_")


class TestConfig(GlobalConfig):
    # JWT_SECRET_KEY: str = (
    #     "4598398cca0a7ecb7c7466fb30e43d4525bb3f5c59974183c8f46724e63ccee7"
    # )
    # JWT_ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_prefix="TEST_")


@lru_cache()
def get_config(env_state: str):
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs[env_state]()


logger.debug(f"Loading config for {BaseConfig().ENV_STATE}")
config = get_config(BaseConfig().ENV_STATE)


# DB configuration
def get_postgres_uri():
    host = config.DB_HOST
    port = 54321 if host == "localhost" else 5432
    password = config.DB_PASSWORD
    user = config.DB_USER
    db_name = config.DB_NAME
    logger.debug(f"Using {config.ENV_STATE}")
    logger.debug(f"Using {db_name}")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


# API configuration
def get_api_url():
    host = config.API_HOST
    port = 8000 if host == "localhost" else 8000
    return f"http://{host}:{port}"
