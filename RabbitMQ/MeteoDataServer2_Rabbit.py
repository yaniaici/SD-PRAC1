#!/usr/bin/env python
import pika
import json
import time
import meteo_utils
import redis


class GlobalData():
    def __init__(self, type, field1, field2, time):
        self.type = type
        self.field1 = field1
        self.field2 = field2
        self.time = time


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
print('[*] Waiting for messages...')

# We create the communication to the Redis server
r = redis.Redis(host='localhost', port=6379, db=0)

# We create a callback function that is going to be called when a message is received
def callback(ch, method, properties, body):
    # We print the received messageGlobalMeteoData
    print(" [x] Received %r" % body)

    # We convert the message to a dictionary
    message = json.loads(body.decode())
    meteo_data = GlobalData(message["type"], message["field1"], message["field2"], message["time"])

    # We create the corresponding data structure
    if message["type"] == 'a':
        print("Meteo Data{ Temperature:" + str(meteo_data.field2) + "         Humidity:" + str(meteo_data.field1))
        print("The time is --> " + str(meteo_data.time))
        meteodata = MeteoData(meteo_data.field2, meteo_data.field1)
        airWellness = meteo_utils.MeteoDataProcessor().process_meteo_data(meteodata)
        print('Result    AirWelness:' + str(airWellness))
        dataToRedis = {
            'type': 'a',
            'humidity': meteo_data.field1,
            'temperature': meteo_data.field1,
            'AirWellness': airWellness,
            'time': meteo_data.time
        }
    elif message["type"] == 'p':
        print("Pollution Data{ CO2:" + str(meteo_data.field1) + "}")
        print("The time is --> " + str(meteo_data.time))
        pollData = PollutionData(meteo_data.field2)
        pollResult = meteo_utils.MeteoDataProcessor().process_pollution_data(pollData)
        print('Result    Pollution:' + str(pollResult))
        dataToRedis = {
            'type': 'p',
            'co2': meteo_data.field1,
            'Pollution': pollResult,
            'time': meteo_data.time
        }
        
    # We convert the data structure to a JSON
    redisJson = json.dumps(dataToRedis)
    print("Data send to redis --> " + redisJson)
    r.lpush(str(meteo_data.time), redisJson)
    print(" [x] Done") 

    # We send an acknowledgment to the server
    ch.basic_ack(delivery_tag=method.delivery_tag)

#Indicates that only works with one message at the same time
channel.basic_qos(prefetch_count=1)
#Indicates that is going to consume messages from the queue = "dataToSever" and with this data is going to do "callback" function
channel.basic_consume(queue='dataToServer', on_message_callback=callback)

#Start consuming from the queue
channel.start_consuming()