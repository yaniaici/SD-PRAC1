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