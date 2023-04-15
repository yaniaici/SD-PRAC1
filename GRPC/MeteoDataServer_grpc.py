import grpc
from concurrent import futures
import SensorData_pb2
import SensorData_pb2_grpc
import meteo_utils
from google.protobuf import empty_pb2
import redis

class SensorDataService (SensorData_pb2_grpc.SensorDataServiceServicer):

    
    # Method that recieves the MeteoData info
    def SendMeteoData(self, request, context):
        print("Received meteo data from sensor " + str(request.sensor_id))
        print("Temperature: " + str(request.temperature))
        print("Humidity: " + str(request.humidity))
        print("Timestamp: " + str(request.timestamp.ToDatetime()))
        service = SensorDataService()
        service.SendToRedisMeteo(request, context)
        return empty_pb2.Empty()
    
    def SendPollutionData(self, request, context):
        print("Received pollution data from sensor " + str(request.sensor_id))
        print("Pollution: " + str(request.co2))
        print("Timestamp: " + str(request.timestamp.ToDatetime()))
        service = SensorDataService()
        service.SendToRedisPollution(request, context)
        return empty_pb2.Empty()
    
    def SendToRedisMeteo(self, request, context):
        service = SensorDataService()
        airwellness = service.ProcessMeteoDataRedis(request)
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        # Add key value pairs to Redis
        r.hset(str(request.sensor_id) , str(request.timestamp), str(airwellness))
        print("Values added to Redis:");
        # We use sensor_id as a key
        print(r.hgetall(str(request.sensor_id)))
        r.close
        return None
    
    def SendToRedisPollution(self, request, context):
        service = SensorDataService()
        pollution_index = service.ProcessPollutionDataRedis(request)
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        # Add key value pairs to Redis
        r.hset(str(request.sensor_id) , str(request.timestamp), str(pollution_index))
        print("Values added to Redis:");
        # We use sensor_id as a key
        print(r.hgetall(str(request.sensor_id)))
        r.close
        return None


    # Process the meteo_data with meteo_utils.py
    def ProcessMeteoData(self, request, context):
        meteo_data = SensorData_pb2.RawMeteoData()
        meteo_data.sensor_id = request.sensor_id
        meteo_data.temperature = request.temperature
        meteo_data.humidity = request.humidity
        meteo_data.timestamp.FromDatetime(request.timestamp.ToDatetime())
        airwellness = meteo_utils.MeteoDataProcessor()
        airwellness_procesado = airwellness.process_meteo_data(meteo_data)
        print("Calculated air wellness index: " + str(airwellness_procesado))
        return SensorData_pb2.AirWellnessCoefficient(airwellness=airwellness_procesado)
    
        # Process the meteo_data with meteo_utils.py  FOR REDIS SERVER
    def ProcessMeteoDataRedis(self, request):
        meteo_data = SensorData_pb2.RawMeteoData()
        meteo_data.sensor_id = request.sensor_id
        meteo_data.temperature = request.temperature
        meteo_data.humidity = request.humidity
        meteo_data.timestamp.FromDatetime(request.timestamp.ToDatetime())
        airwellness = meteo_utils.MeteoDataProcessor()
        airwellness_procesado = airwellness.process_meteo_data(meteo_data)
        print("Calculated air wellness index: " + str(airwellness_procesado))
        return SensorData_pb2.AirWellnessCoefficient(airwellness=airwellness_procesado)
    
    def ProcessPollutionData(self, request, context):
        pollution_data = SensorData_pb2.RawPollutionData()
        pollution_data.sensor_id = request.sensor_id
        pollution_data.co2 = request.co2
        pollution_data.timestamp.FromDatetime(request.timestamp.ToDatetime())
        pollution_index = meteo_utils.MeteoDataProcessor()
        pollution_index_procesado = pollution_index.process_pollution_data(pollution_data)
        print("Calculated pollution index: " + str(pollution_index_procesado))
        return SensorData_pb2.PollutionCoefficient(pollution=pollution_index_procesado)
    
    def ProcessPollutionDataRedis(self, request):
        pollution_data = SensorData_pb2.RawPollutionData()
        pollution_data.sensor_id = request.sensor_id
        pollution_data.co2 = request.co2
        pollution_data.timestamp.FromDatetime(request.timestamp.ToDatetime())
        pollution_index = meteo_utils.MeteoDataProcessor()
        pollution_index_procesado = pollution_index.process_pollution_data(pollution_data)
        print("Calculated pollution index: " + str(pollution_index_procesado))
        return SensorData_pb2.PollutionCoefficient(pollution=pollution_index_procesado)
    
    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        SensorData_pb2_grpc.add_SensorDataServiceServicer_to_server(SensorDataService(), server)
        server.add_insecure_port(f"[::]:50051")
        print("Server started on port 50051")
        server.start()
        server.wait_for_termination()

if __name__ == "__main__":
    server = SensorDataService()
    server.serve()