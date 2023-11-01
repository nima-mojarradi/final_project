from django.core.management.base import BaseCommand
from user.consumer import register_consumer
class Command(BaseCommand):
    def handle(self, *args, **options):
        register_consumer()