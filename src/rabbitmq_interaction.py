import sys
import os
import pika


def enqueue_to_rabbitmq(id: int):
    """ Uses the cloudAMPQ API to enqueue the given 'id' to the queue
    
    Args:
        id (int): The given id
    
    """
    
    # URL to your AMPQ account servece:
    url_parameters = pika.URLParameters("")
    url_parameters.socket_timeout = 10
    connection = pika.BlockingConnection(url_parameters)
    channel = connection.channel()
    channel.queue_declare(queue="ids")
    channel.basic_publish(exchange="", routing_key="ids", body=str(id))
    print(f"Sent the id to the queue: {id}")
    connection.close()


class RabbitMqListener:
    """ RabbitMqListener is responsible for subscribing on the RabbigMQ service
        to get the newly enqueued messages.
    """
    def __init__(self, callback):
        try:
        
            # URL to your AMPQ account servece:
            url_parameters = pika.URLParameters("")
            url_parameters.socket_timeout = 10
            connection = pika.BlockingConnection(url_parameters)
            channel = connection.channel()
            channel.queue_declare(queue="ids")
            channel.basic_consume(queue="ids", on_message_callback=callback, auto_ack=True)
            print("Connected to the service. Waiting for messages... Press Ctrl+C to exit")
            channel.start_consuming()
        except KeyboardInterrupt:
            print("Interrupted, clearing up")
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
