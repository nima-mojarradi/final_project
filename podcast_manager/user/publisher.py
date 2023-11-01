import pika
import time
import os
# from podcast_manager.settings import ALLOWED_HOSTS

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# credintial = pika.PlainCredentials(username='guest', password='guest')

def publisher(queue, body):
    connection = pika.BlockingConnection(pika.URLParameters('amqp://guest:guest@rabbitmq:5672'))
    channel = connection.channel()

    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange="", routing_key=queue, body=body)
    print('finished'+'*'*100)

    connection.close()