from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.utils.log import get_task_logger
from .views import RequestUrl
from celery import shared_task

logger = get_task_logger(__name__)
app = Celery('retry_task', broker='redis://localhost:6380')

@app.task(bind=True, max_retries=3)
def retry_task(self, url):
    try:
        RequestUrl(url=url)
    except Exception as e:
        logger.error(f'Task failed: {e}')
        raise self.retry(exc=e)
    

@shared_task
def parse_channel_priodic(url):
    RequestUrl(url)