import pika
import os
# from podcast_manager.settings import ALLOWED_HOSTS
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


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


def login_callback(ch, method, properties, body):
    print(f'Recieved{body}')
    print("2"*100)
    print(method)
    print("3"*100)
    print(properties)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def register_callback(ch, method, properties, body):
    print(f'Recieved{body}')
    print("4"*100)
    print(method)
    print("5"*100)
    print(properties)
    ch.basic_ack(delivery_tag=method.delivery_tag)