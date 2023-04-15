import pika
import json
import time
import meteo_utils
import redis


class GlobalData():
    def __init__(self, type, field1, field2):
        self.type = type
        self.field1 = field1
        self.field2 = field2


# We declare data structures directly on the server

class MeteoData:
    def __init__(self, temperature, humidity):
        self.temperature = temperature
        self.humidity = humidity

class PollutionData:
    def __init__(self, co2):
        self.co2 = co2


# We create the communication to the RabbitMQ server and specify the queue that is going to use
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='clientToServer', durable=True)
print('Waiting for messages...')

# We create the communication to the Redis server
r = redis.Redis(host='localhost', port=6380, db=0)

# We create a callback function that is going to be called when a message is received
def callback(ch, method, properties, body):
    # We print the received message
    print(" [x] Received %r" % body)

    # We convert the message to a dictionary
    message = json.loads(body)

    # We create the corresponding data structure
    if message["type"] == 'a':
        meteo_data = MeteoData(message["field1"], message["field2"])
        print(meteo_data.temperature)
        print(meteo_data.humidity)
        # We store the data in the Redis server
        r.hset(1, meteo_data.temperature, meteo_data.humidity)
    elif message["type"] == 'p':
        pollution_data = PollutionData(message["field1"])
        print(pollution_data.co2)
        # We store the data in the Redis server
        r.hset(2, pollution_data.co2)

    # We send an acknowledgment to the server
    ch.basic_ack(delivery_tag=method.delivery_tag)

#Indicates that only works with one message at the same time
channel.basic_qos(prefetch_count=1)
#Indicates that is going to consume messages from the queue = "dataToSever" and with this data is going to do "callback" function
channel.basic_consume(queue='dataToServer', on_message_callback=callback)

#Start consuming from the queue
channel.start_consuming()