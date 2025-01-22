from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.conf.update(
    broker_url=settings.BROKER_URL,  # Адрес брокера сообщений, например, Redis
    result_backend="django-db",  # Бэкенд для хранения результатов
    task_serializer="json",  # Формат сериализации задач
    result_serializer="json",  # Формат сериализации результатов
    accept_content=["json"],  # Принимаемые типы содержимого
    timezone=settings.TIME_ZONE,  # Часовой пояс
    enable_utc=True,  # Использование UTC времени
    beat_scheduler="django_celery_beat.schedulers:DatabaseScheduler",  # Планировщик задач Celery Beat
    broker_connection_retry_on_startup=True,  # Повторные попытки подключения к брокеру при запуске
)

app.autodiscover_tasks()

# celery -A core.celery worker -l info -c 2 -P eventlet
# celery -A core beat -l info
# celery -A core flower
