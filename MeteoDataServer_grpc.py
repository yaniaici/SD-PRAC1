import grpc
from concurrent import futures
import SensorData_pb2
import SensorData_pb2_grpc
import meteo_utils

class SensorDataService (SensorData_pb2_grpc.SensorDataServiceServicer):
    def ProcessMeteoData(self, request, context):
        temperature = request.temperature
        humidity = request.humidity

        # Call the meteo_utils function to process the data
        airwellness = meteo_utils.process_meteo_data(temperature, humidity)

        # Create a airweellnesscoefficient object
        response = SensorData_pb2.AirWellnessCoefficient()
        response.airwellnesscoefficient = airwellness

        return response
    
    def SendMeteoData(self, request, context):
        print("Received meteo data from sensor " + str(request.sensor_id))
        print("Temperature: " + str(request.temperature))
        print("Humidity: " + str(request.humidity))
        print("Timestamp: " + str(request.timestamp.ToDatetime()))
        return SensorData_pb2.Empty()
    
    
    
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