import requests
import xml.etree.ElementTree as ET
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import EpisodeData, PodcastData, RSSLink
import time
from celery import Celery

def ParseChannel(url):
    response = requests.get(url)
    root = ET.fromstring(response.content)
    title = root.find('channel/title').text
    description = root.find('channel/description').text
    link = root.find('channel/link').text
    language = root.find('language')
    itunes_author = root.find('.//{http://www.itunes.com/dtds/podcast-1.0.dtd}author').text
    itunes_duration = root.find('.//{http://www.itunes.com/dtds/podcast-1.0.dtd}:duration').text
    images = root.find('.//{http://www.itunes.com/dtds/podcast-1.0.dtd}:image').text
    itunes_category = root.find('.//{http://www.itunes.com/dtds/podcast-1.0.dtd}:category').text
    rss_link, created = RSSLink.objects.get_or_create(url=url)

    rss_feed_items = PodcastData.objects.get_or_create(
                title=title,
                description=description,
                link=link,
                itunes_author=itunes_author.text if itunes_author is not None else None,
                itunes_duration=itunes_duration.text if itunes_duration is not None else None,
                rss_link = rss_link,
                )
    items = root.findall('channel/item')
    items_list = []
    for item in items:
        title = item.find('title').text
        description = item.find('description').text
        itunes_author = item.find('.//{http://www.itunes.com/dtds/podcast-1.0.dtd}author').text if item.find('.//{http://www.itunes.com/dtds/podcast-1.0.dtd}author') is not None else None
        itunes_duration = item.find('.//{http://www.itunes.com/dtds/podcast-1.0.dtd}:duration').text if item.find('.//{http://www.itunes.com/dtds/podcast-1.0.dtd}:duration') is not None else None
        itunes_images = item.find('.//{http://www.itunes.com/dtds/podcast-1.0.dtd}:image').text if item.find('.//{http://www.itunes.com/dtds/podcast-1.0.dtd}:image') is not None else None
        guid = item.find('guid').text
        rss_feed_item = EpisodeData(
            title=title,
            description=description,
            link=link,
            itunes_author=itunes_author,
            itunes_duration=itunes_duration,
            guid = guid,
            podcast=rss_feed_items[0]
            )
        items_list.append(rss_feed_item)
    EpisodeData.objects.bulk_create(items_list, ignore_conflicts=True)