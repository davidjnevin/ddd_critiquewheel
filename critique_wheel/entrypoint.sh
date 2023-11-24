#!/bin/bash

set -e
set -o nounset

postgres_ready() {
    python << END
import sys

from psycopg2 import connect
from psycopg2.errors import OperationalError

try:
    connect(
        dbname="${DB_NAME}",
        user="${DB_USER}",
        password="${DB_PASSWORD}",
    )
except OperationalError:
    sys.exit(-1)
END
}
wait_other_containers() {
	until postgres_ready; do
		>&2 echo "Waiting for PostgreSQL to become available..."
		sleep 5
	done
	>&2 echo "PostgreSQL is available"

}


cd /app


case $1 in
	"bash")
		bash;;
	"server")
		wait_other_containers ;\
	 	if [ "$FASTAPI_DEBUG" = "true" ]; then
        uvicorn \
            critique_wheel.fast_api:app \
			--host 0.0.0.0 \
            --port 8000 \
            --workers 2 \
            --reload \
            --log-level debug
		else
			uvicorn \
				critique_wheel.fast_api:app \
				--host 0.0.0.0 \
				--port 8000 \
				--workers 2
		fi
	;;
	"test")
		wait_other_containers ;\
		pytest
		;;
	"test-current")
		wait_other_containers ;\
		pytest -vv -m current
		;;
	"lint")
		isort critique_wheel tests
		ruff critique_wheel tests
		mypy critique_wheel
		;;
	"*")
		exec "$@"
		;;
esac


