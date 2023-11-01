from django.core.management.base import BaseCommand
from user.consumer import update_invalid_podcast_consumer
class Command(BaseCommand):
    def handle(self, *args, **options):
        update_invalid_podcast_consumer()