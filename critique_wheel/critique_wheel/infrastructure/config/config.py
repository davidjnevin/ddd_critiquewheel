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
FORMAT_UUID_FOR_SQLITE = DATABASE_TYPE == "sqlite"
