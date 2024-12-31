#!/bin/sh
set -e

if [ "$1" = "webserver" ]; then

	python manage.py migrate
	python manage.py collectstatic --no-input --clear

	gunicorn --workers=2 --bind=0.0.0.0:8000 voidmon.wsgi
elif [ "$1" = "celery-worker" ]; then
    exec celery -A voidmon worker --concurrency 2 --loglevel=info
elif [ "$1" = "celery-beat" ]; then
    exec celery -A voidmon beat --loglevel=info
else
    echo "Unknown command: $1"
    exit 1
fi
