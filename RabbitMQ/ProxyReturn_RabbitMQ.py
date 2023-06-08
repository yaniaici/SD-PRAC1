import pika
import json
import redis
import threading
import time


air_wellness = 0
mean_air_wellness = 0
pollution_data = 0
mean_pollution_data = 0
keysG = []

# We create the communication to the RabbitMQ server and specify the queue that is going to use

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()


channel.exchange_declare(exchange='logs', exchange_type='fanout')

# We create the communication to the Redis server
r = redis.Redis(host='localhost', port=6379, db=0)

def parse_data():
    
    global air_wellness, pollution, mean_air_wellness, mean_pollution_data, keysG
    
    while True:
        keycount = r.dbsize()
        keys = r.keys()
        dictAir = []
        dictPol = []
        
        if keycount > 0:
            
            for key in keys:
                key = key.decode('utf-8')
                print("Key: ", key)
                data = r.lrange(key, 0, -1)
                print("Data1: ", data)
                data = [x.decode('utf-8') for x in data]
                for string in data:
                    d = json.loads(string)
                    if d['type'] == 'a':
                        dictAir.append(d['AirWellness'])
                    elif d['type'] == 'p':
                        dictPol.append(d['Pollution'])
            r.delete(key)
            
            print("dictAir: ", dictAir)
            print("dictPol: ", dictPol)
            
            if len(dictAir) > 0:
                mean_air_wellness = sum(dictAir) / len(dictAir)
            else:
                mean_air_wellness = 0
            if len(dictPol) > 0:
                mean_pollution_data = sum(dictPol) / len(dictPol)
            else:
                mean_pollution_data = 0
                
            print("Mean Air Wellness: ", mean_air_wellness)
            print("Mean Pollution: ", mean_pollution_data)
            
            air_wellness = dictAir
            pollution = dictPol
            
            keysG = keys
            keysG = [x.decode('utf-8') for x in keysG]
            keysG = [str(x) for x in keysG]
            keysG = [x.replace("\n", "") for x in keysG]
            
            
            message = {
            'airMean': mean_air_wellness,
            'pollMean': mean_pollution_data,
            }
            
            messageToSend = json.dumps(message)
            
            channel.basic_publish(exchange='logs', routing_key='', body=messageToSend)
            print(" [x] Sent %r" % messageToSend)
            time.sleep(5)
            
            
redis_thread = threading.Thread(target=parse_data)

redis_thread.start()

redis_thread.join()

            
                       