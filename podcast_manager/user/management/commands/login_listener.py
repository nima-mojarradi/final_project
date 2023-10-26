from django.core.management.base import BaseCommand
from user.consumer import login_consumer
class Command(BaseCommand):
    # help = 'Launches Consumer for login message : RabbitMQ'
    def handle(self, *args, **options):
        login_consumer()