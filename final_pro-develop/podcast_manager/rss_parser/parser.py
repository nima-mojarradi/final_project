import requests
import xml.etree.ElementTree as ET
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ModelParser
import time
from celery import Celery
from .models import ModelParser
app = Celery('tasks', broker='amqp://localhost')
@app.task(bind=True, max_retries=3)
def ParseRssFeed(self, url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        root = ET.fromstring(response.content)
        items = []
        for item in root.iter('item'):
            title = item.find('title').text
            description = item.find('description').text
            link = item.find('link').text
            itunes_author = item.find('.//{http://www.itunes.com/dtds/podcast-1.0.dtd}author')
            itunes_duration = item.find('.//{http://www.itunes.com/dtds/podcast-1.0.dtd}:duration')
            itunes_images = item.find('.//{http://www.itunes.com/dtds/podcast-1.0.dtd}:image')
            itunes_category = item.find('.//{http://www.itunes.com/dtds/podcast-1.0.dtd}:category')
            rss_feed_item = ModelParser(
                title=title,
                description=description,
                link=link,
                itunes_author=itunes_author.text if itunes_author is not None else None,
                itunes_duration=itunes_duration.text if itunes_duration is not None else None,
                category=itunes_category
                )
            rss_feed_item.save()
            items.append({
            'title': title,
            'description': description,
            'link': link,
            'itunes_author': itunes_author.text if itunes_author is not None else None,
            'itunes_duration': itunes_duration.text if itunes_duration is not None else None,
            'itunes_image': itunes_images.text if itunes_images is not None else None,
        })
        return items
    except requests.RequestException as e:
        self.retry(exc=e, countdown=min(self.countdown * 2, 60))