import redis
import statistics
import grpc
import SensorData_pb2
import SensorData_pb2_grpc

class ProxyReturn:
    def __init__(self):
        # Create a gRPC channel to communicate with terminal
        self.channel = grpc.insecure_channel('localhost:50055')
        
        # Create stubs for sending air pollution and air wellness data
        self.pollution_stub = SensorData_pb2_grpc.ProxyReturnServiceStub(self.channel)
        self.wellness_stub = SensorData_pb2_grpc.ProxyReturnServiceStub(self.channel)

    def get_airwellness_values(self):
        # Create a Redis client
        r = redis.StrictRedis(host='localhost', port=6379, db=0)

        # Extract airwellness values
        airwellness_values = r.hvals('1')

        print(airwellness_values)

        parsed_values = []
        for value in airwellness_values:
            parsed_value = float(value.decode().split(': ')[1].strip())
            parsed_values.append(parsed_value)

        print(parsed_values)
        return parsed_values
    
    def get_airwellness_mean(self):
        airwellness_values = self.get_airwellness_values()
        return statistics.mean(airwellness_values)
    
    def get_airpollution_values(self):
        # Create a Redis client
        r = redis.StrictRedis(host='localhost', port=6379, db=0)

        # Extract airpollution values
        airpollution_values = r.hvals('2')

        print(airpollution_values)

        parsed_values = []
        for value in airpollution_values:
            parsed_value = float(value.decode().split(': ')[1].strip())
            parsed_values.append(parsed_value)
        
        print(parsed_values)
        return parsed_values

    def get_airpollution_mean(self):
        airpollution_values = self.get_airpollution_values()
        return statistics.mean(airpollution_values)
    
    def send_air_pollution(self):
        air_pollution = self.get_airpollution_mean()
        air_pollution_data = SensorData_pb2.PollutionCoefficient()
        air_pollution_data.pollution = air_pollution
        self.pollution_stub.SendAirPollutionCoefficient(air_pollution_data)

    def send_air_wellness(self):
        air_wellness = self.get_airwellness_mean()
        air_wellness_data = SensorData_pb2.AirWellnessCoefficient()
        air_wellness_data.airwellness = air_wellness
        self.wellness_stub.SendAirWellnessCoefficient(air_wellness_data)

if __name__ == "__main__":
    proxy = ProxyReturn()
    proxy.send_air_pollution()
    proxy.send_air_wellness()
