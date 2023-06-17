#!/usr/bin/env python
import pika
import json

# Creamos la conexión al servidor RabbitMQ y especificamos la cola que vamos a utilizar
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')
print('Waiting for messages...')

# Creamos una función de devolución de llamada que se ejecutará al recibir un mensaje
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)


def callback(ch, method, properties, body):
    data = json.loads(body.decode())
    if data['airMean'] != 0:
        print("\033[92mAirwellness mean:\033[0m", data['airMean'])
    if data['pollMean'] != 0:
        print("\033[91mPollution mean:\033[0m", data['pollMean'])


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
