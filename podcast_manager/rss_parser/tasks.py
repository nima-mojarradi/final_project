from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.utils.log import get_task_logger
from .parser import ParseChannel
from .models import RSSLink
from celery import shared_task
from celery.schedules import crontab


logger = get_task_logger(__name__)


@shared_task(autoretry_for=(Exception,), max_retries=3, retry_backoff=True)
def parse_rss_links():
    for link in RSSLink.objects.all():
        ParseChannel(link.url)
    
    