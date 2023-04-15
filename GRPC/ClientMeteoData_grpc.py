import grpc
import SensorData_pb2
import SensorData_pb2_grpc
import LoadBalancer_pb2_grpc
import LoadBalancer_pb2
from google.protobuf import empty_pb2
from datetime import datetime
import meteo_utils

class Client:

    def __init__(self):
        # Create a gRPC channel to communicate with the load balancer
        lb_channel = grpc.insecure_channel('localhost:50053')
        self.lb_stub = LoadBalancer_pb2_grpc.LoadBalancerServiceStub(lb_channel)

    def send_meteo_data(self, sensor_id, temperature, humidity, timestamp):
        # Get the server address from LB
        server_address = self.lb_stub.ChooseServer(empty_pb2.Empty()).serveraddress

        # Create a gRPC channel to communicate with the server
        channel = grpc.insecure_channel(server_address)

        # Create a stub for the SensorData service
        stub = SensorData_pb2_grpc.SensorDataServiceStub(channel)

        # Create a RawMeteoData object and set fields
        meteo_data = SensorData_pb2.RawMeteoData()
        meteo_data.sensor_id = sensor_id
        meteo_data.temperature = temperature
        meteo_data.humidity = humidity
        meteo_data.timestamp.FromDatetime(timestamp)

        # Call the RPC method to send the meteo data
        stub.SendMeteoData(meteo_data)

if __name__ == "__main__":
    client = Client()
    detector = meteo_utils.MeteoDataDetector()
    sensor_id = 1
    temperature = detector.gen_temperature()
    humidity = detector.gen_humidity()
    timestamp = datetime.now()
    client.send_meteo_data(sensor_id, temperature, humidity, timestamp)




