#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input

python -m celery -A core.celery worker -l info -c 2 -P eventlet &
python -m celery -A core beat -l info &

# gunicorn --bind 0.0.0.0:8000 core.asgi -w 4 -k uvicorn.workers.UvicornWorker # с возможностью указания количества воркеров
uvicorn core.asgi:application --host 0.0.0.0 --port 9090