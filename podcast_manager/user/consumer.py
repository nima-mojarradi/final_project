import pika
from rss_parser.models import Notification
import os
import json
# from podcast_manager.settings import ALLOWED_HOSTS
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'podcast_manager.settings')


def login_consumer():
    conn = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    ch = conn.channel()
    ch.queue_declare('login')
    ch.basic_consume(queue='login', on_message_callback=login_callback)
    ch.start_consuming()
    
def register_consumer():
    conn = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    ch = conn.channel()
    ch.queue_declare('register')
    ch.basic_consume(queue='register', on_message_callback=register_callback)
    ch.start_consuming()

def update_invalid_podcast_consumer():
    conn = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    ch = conn.channel()
    ch.queue_declare('update_invalid_podcast')
    ch.basic_consume(queue='update_invalid_podcast', on_message_callback=update_invalid_podcast_callback)
    ch.start_consuming()

def update_valid_podcast_consumer():
    conn = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    ch = conn.channel()
    ch.queue_declare('update_valid_podcast')
    ch.basic_consume(queue='update_valid_podcast', on_message_callback=update_valid_podcast_callback)
    ch.start_consuming()


def login_callback(ch, method, properties, body):
    body=json.loads(body)
    print(f'Recieved{body}')
    print("2"*100)
    print(method)
    print("3"*100)
    print(properties)
    Notification.objects.create(user_id=body['user_id'], notif_type='login', message=body['massage'])
    ch.basic_ack(delivery_tag=method.delivery_tag)


def register_callback(ch, method, properties, body):
    body=json.loads(body)
    print(f'Recieved{body}')
    print("4"*100)
    print(method)
    print("5"*100)
    print(properties)
    Notification.objects.create(user_id=body['user_id'], notif_type='register', message=body['massage'])
    ch.basic_ack(delivery_tag=method.delivery_tag)


def update_invalid_podcast_callback(ch, method, properties, body):
    body=json.loads(body)
    print(f'Recieved{body}')
    print("6"*100)
    print(method)
    print("7"*100)
    print(properties)
    Notification.objects.create(user_id=body['user_id'], notif_type='request_to_url', message=body['massage'])
    ch.basic_ack(delivery_tag=method.delivery_tag)


def update_valid_podcast_callback(ch, method, properties, body):
    body=json.loads(body)
    print(f'Recieved{body}')
    print("8"*100)
    print(method)
    print("9"*100)
    print(properties)
    Notification.objects.create(user_id=body['user_id'], notif_type='request_to_url', message=body['massage'])
    ch.basic_ack(delivery_tag=method.delivery_tag)