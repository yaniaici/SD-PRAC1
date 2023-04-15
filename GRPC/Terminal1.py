import grpc
import SensorData_pb2
import SensorData_pb2_grpc
from concurrent import futures
from google.protobuf import empty_pb2
from tabulate import tabulate


class SensorDataReceiver(SensorData_pb2_grpc.ProxyReturnServiceServicer):

    def SendAirPollutionCoefficient(self, request, context):
        print("\nReceived air pollution coefficient:")
        print(tabulate([['Pollution Coefficient', request.pollution]], headers=['Parameter', 'Value'], tablefmt='fancy_grid'))
        return empty_pb2.Empty()

    def SendAirWellnessCoefficient(self, request, context):
        print("\nReceived air wellness coefficient:")
        print(tabulate([['Air Wellness Coefficient', request.airwellness]], headers=['Parameter', 'Value'], tablefmt='fancy_grid'))
        return empty_pb2.Empty()

if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    SensorData_pb2_grpc.add_ProxyReturnServiceServicer_to_server(SensorDataReceiver(), server)
    server.add_insecure_port('[::]:50055')
    print("Server on 50055")
    server.start()
    server.wait_for_termination()
