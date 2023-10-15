from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.utils.log import get_task_logger
from .parser import ParseChannel
from .models import RSSLink
from celery import shared_task
from celery.schedules import crontab
# from celery import periodic_task

logger = get_task_logger(__name__)
app = Celery('retry_task', broker='redis://localhost:6380')

@shared_task
def parse_rss_links():
    for link in RSSLink.objects.all():
        ParseChannel(link.url)
    

# @periodic_task(
#     run_every=(crontab(minute='*/15')),
#     name="parse_rss_links_every_15_minutes",
#     ignore_result=True
# )
# def parse_rss_links_every_15_minutes():
#     for link in RSSLink.objects.all():
#         ParseChannel(link.url)
