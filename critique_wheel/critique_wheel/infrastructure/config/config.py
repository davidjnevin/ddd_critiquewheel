import os

from dotenv import load_dotenv

# Feature flag toggle for testing using SQLite
# If True, UUIDs will be formatted for SQLite
# If False, UUIDs will be formatted for PostgreSQL
# This is because SQLite does not support UUIDs
# and PostgreSQL does

# Load environment variables from .env file
load_dotenv()

# Database configuration
DATABASE_TYPE = os.getenv("DATABASE_TYPE")
# Feature flags based on the database type
TESTING_USING_SQLITE = DATABASE_TYPE == "sqlite"

# DB configuration
def get_postgres_uri():
    host = os.getenv("DB_HOST", "localhost")
    port = 54321 if host == "localhost" else 5432
    password = os.getenv("DB_PASSWORD", "abc123")
    user = os.getenv("DB_USER", "abc123")
    db_name = os.getenv("DB_NAME", "abc123")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

# API configuration
def get_api_url():
    host = os.getenv("API_HOST", "localhost")
    port = 5005 if host == "localhost" else 80
    return f"http://{host}:{port}"
