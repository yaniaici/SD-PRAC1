#!usr/bin/env python
# docker run -it -rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management

import pika
import json
import time
import meteo_utils

# Data structure used for the server
class GlobalMeteoData:
    def __init__(self, type, field1, field2, time):
        self.type= type
        self.field1 = field1
        self.field2 = field2
        self.time = time


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# We use durable=true for error management purposes
channel.queue_declare(queue='clientToServer', durable=True)

sensor = meteo_utils.MeteoDataDetector()
meteo_data = sensor.analyze_air()
print(meteo_data["temperature"])
print(meteo_data["humidity"])
# We create directly a dictionary
pollution_data = sensor.analyze_pollution()
print(pollution_data["co2"])

# We create a GlobalMeteoData object
global_meteo_data = GlobalMeteoData('a', field1=meteo_data["temperature"], field2=meteo_data["humidity"], time=time.localtime())
message = json.dumps(vars(global_meteo_data))

# We send the data
channel.basic_publish(exchange='', routing_key='clientToServer', body=message, properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

print(" [x] Sent %r" % message)

# We create a GlobalMeteoData object
global_meteo_data = GlobalMeteoData('p', field1=pollution_data["co2"], field2=0, time=time.localtime())
message = json.dumps(vars(global_meteo_data))
channel.basic_publish(exchange='', routing_key='clientToServer', body=message, properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

print(" [x] Sent %r" % message)

connection.close()