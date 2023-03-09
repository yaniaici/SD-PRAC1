import grpc
import LoadBalancer_pb2
import LoadBalancer_pb2_grpc
import random

class LoadBalancerServicer(LoadBalancer_pb2_grpc.LoadBalancerServiceServicer):
    def __init__(self, server_addresses):
        self.server_addresses = server_addresses

    def ChooseServer(self, request, context):
        server_address = random.choice(self.server_addresses)
        return LoadBalancer_pb2.ServerAddress(server_address=server_address)
    
    def serve():
        server_addresses = ['localhost:50051', 'localhost:50052']
        channel = grpc.server(grpc.insecure_channel('localhost:50053'))
        server = grpc.server(channel)

        LoadBalancer_pb2_grpc.add_LoadBalancerServiceServicer_to_server(LoadBalancerServicer(server_addresses), server)

        server.add_secure_port('[::]:50053')
        server.start()
        print("Load balancer started on port 50053")
        server.wait_for_termination()

    if __name__ == '__main__':
        serve()