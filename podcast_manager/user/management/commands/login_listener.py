from django.core.management.base import BaseCommand
from user.consumer import login_consumer
class Command(BaseCommand):
    def handle(self, *args, **options):
        login_consumer()