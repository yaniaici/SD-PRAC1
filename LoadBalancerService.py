import grpc
import LoadBalancer_pb2
import LoadBalancer_pb2_grpc
from concurrent import futures

class LoadBalancerServicer(LoadBalancer_pb2_grpc.LoadBalancerServiceServicer):
    def __init__(self, server_addresses):
        self.server_addresses = server_addresses
        self.current_server = 0

    def ChooseServer(self, request, context):
        server_address = self.server_addresses[self.current_server]
        print("Server chosen by LoadBalancer: ", server_address)
        self.current_server = (self.current_server + 1) % len(self.server_addresses)
        return LoadBalancer_pb2.ServerAddress(serveraddress=server_address)

def serve():
    server_addresses = ['localhost:50051']
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    LoadBalancer_pb2_grpc.add_LoadBalancerServiceServicer_to_server(LoadBalancerServicer(server_addresses), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("Load balancer started on port 50053")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
