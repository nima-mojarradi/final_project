import pika
import time
import os
import json
# from podcast_manager.settings import ALLOWED_HOSTS

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'podcast_manager.settings')
# credintial = pika.PlainCredentials(username='guest', password='guest')

def publisher(queue, body):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', heartbeat=60))
    channel = connection.channel()

    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange="", routing_key=queue, body=json.dumps(body))
    print('finished'+'*'*100)

    connection.close()