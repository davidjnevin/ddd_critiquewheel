#!/bin/bash

set -e
set -o nounset

cd /app


case $1 in
	"bash")
		bash;;
	# "server")
	# 	;;
	"test")
		pytest
		;;
	"test-current")
		pytest -vv -m current
		;;
	"lint")
		isort --check-only critique_wheel tests
		black --check  critique_wheel tests
		flake8 critique_wheel tests
		mypy critique_wheel
		;;
	"*")
		exec "$@"
		;;
esac


