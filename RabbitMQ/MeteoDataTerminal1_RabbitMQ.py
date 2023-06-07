#!/usr/bin/env python
import pika
import json

# We create the communication to the RabbitMQ server and specify the queue that is going to use
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')
print('Waiting for messages...')

# We create a callback function that is going to be called when a message is received
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)

def callback(ch, method, properties, body):
    data = json.loads(body.decode())
    if not data ['airMean'] == 0:
        print("Airwellness mean: " + str(data['airMean']))
    if not data ['pollMean'] == 0:
        print ("Pollution mean: " + str(data['pollMean']))
        
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()