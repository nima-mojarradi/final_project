from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'podcast_manager.settings')

app = Celery("podcast_manager")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'podcast-parse-task': {
        'task': 'rss_parser.tasks.parse_rss_links',
        'schedule': crontab(hour=12, minute=0),
    },
}