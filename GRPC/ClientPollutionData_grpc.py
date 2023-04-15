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

    def send_pollution_data(self, sensor_id, co2, timestamp):
        # Get the server address from LB
        server_address = self.lb_stub.ChooseServer(empty_pb2.Empty()).serveraddress

        # Create a gRPC channel to communicate with the server
        channel = grpc.insecure_channel(server_address)

        # Create a stub for the SensorData service
        stub = SensorData_pb2_grpc.SensorDataServiceStub(channel)

        # Create a RawPollutionData object and set fields
        pollution_data = SensorData_pb2.RawPollutionData()
        pollution_data.sensor_id = sensor_id
        pollution_data.co2 = co2
        pollution_data.timestamp.FromDatetime(timestamp)

        # Call the RPC method to send the pollution data
        stub.SendPollutionData(pollution_data)

if __name__ == "__main__":
    client = Client()
    detector = meteo_utils.MeteoDataDetector()
    sensor_id = 2
    co2 = int(detector.gen_co2())
    timestamp = datetime.now()
    client.send_pollution_data(sensor_id, co2, timestamp)


