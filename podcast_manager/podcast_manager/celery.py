from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
import settings
import logging
from celery.signals import setup_logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'podcast_manager.settings')

app = Celery("podcast_manager")

app.config_from_object("django.conf:settings", namespace="CELERY")



@setup_logging.connect
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig  # noqa

    dictConfig(settings.LOGGING)

app.autodiscover_tasks()

logging.getLogger("celery").addHandler(logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs/celery.log')))

