from __future__ import absolute_import, unicode_literals
from celery import shared_task

@shared_task(bind=True, retry_limit=5, )
def update_priodic():
    pass