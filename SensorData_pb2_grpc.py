# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import SensorData_pb2 as SensorData__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class SensorDataServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetSensorData = channel.unary_unary(
                '/SensorDataService/GetSensorData',
                request_serializer=SensorData__pb2.SensorRequest.SerializeToString,
                response_deserializer=SensorData__pb2.SensorResponse.FromString,
                )
        self.SendMeteoData = channel.unary_unary(
                '/SensorDataService/SendMeteoData',
                request_serializer=SensorData__pb2.RawMeteoData.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.SendPollutionData = channel.unary_unary(
                '/SensorDataService/SendPollutionData',
                request_serializer=SensorData__pb2.RawPollutionData.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.ProcessMeteoData = channel.unary_unary(
                '/SensorDataService/ProcessMeteoData',
                request_serializer=SensorData__pb2.RawMeteoData.SerializeToString,
                response_deserializer=SensorData__pb2.AirWellnessCoefficient.FromString,
                )
        self.ProcessPollutionData = channel.unary_unary(
                '/SensorDataService/ProcessPollutionData',
                request_serializer=SensorData__pb2.RawPollutionData.SerializeToString,
                response_deserializer=SensorData__pb2.PollutionCoefficient.FromString,
                )
        self.GetAirwellnessCoefficient = channel.unary_unary(
                '/SensorDataService/GetAirwellnessCoefficient',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=SensorData__pb2.AirWellnessCoefficient.FromString,
                )


class SensorDataServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetSensorData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendMeteoData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendPollutionData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ProcessMeteoData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ProcessPollutionData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAirwellnessCoefficient(self, request, context):
        """Returns the airwellness coefficient of the server
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SensorDataServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetSensorData': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSensorData,
                    request_deserializer=SensorData__pb2.SensorRequest.FromString,
                    response_serializer=SensorData__pb2.SensorResponse.SerializeToString,
            ),
            'SendMeteoData': grpc.unary_unary_rpc_method_handler(
                    servicer.SendMeteoData,
                    request_deserializer=SensorData__pb2.RawMeteoData.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'SendPollutionData': grpc.unary_unary_rpc_method_handler(
                    servicer.SendPollutionData,
                    request_deserializer=SensorData__pb2.RawPollutionData.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'ProcessMeteoData': grpc.unary_unary_rpc_method_handler(
                    servicer.ProcessMeteoData,
                    request_deserializer=SensorData__pb2.RawMeteoData.FromString,
                    response_serializer=SensorData__pb2.AirWellnessCoefficient.SerializeToString,
            ),
            'ProcessPollutionData': grpc.unary_unary_rpc_method_handler(
                    servicer.ProcessPollutionData,
                    request_deserializer=SensorData__pb2.RawPollutionData.FromString,
                    response_serializer=SensorData__pb2.PollutionCoefficient.SerializeToString,
            ),
            'GetAirwellnessCoefficient': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAirwellnessCoefficient,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=SensorData__pb2.AirWellnessCoefficient.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'SensorDataService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SensorDataService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetSensorData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SensorDataService/GetSensorData',
            SensorData__pb2.SensorRequest.SerializeToString,
            SensorData__pb2.SensorResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendMeteoData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SensorDataService/SendMeteoData',
            SensorData__pb2.RawMeteoData.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendPollutionData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SensorDataService/SendPollutionData',
            SensorData__pb2.RawPollutionData.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ProcessMeteoData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SensorDataService/ProcessMeteoData',
            SensorData__pb2.RawMeteoData.SerializeToString,
            SensorData__pb2.AirWellnessCoefficient.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ProcessPollutionData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SensorDataService/ProcessPollutionData',
            SensorData__pb2.RawPollutionData.SerializeToString,
            SensorData__pb2.PollutionCoefficient.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAirwellnessCoefficient(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SensorDataService/GetAirwellnessCoefficient',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            SensorData__pb2.AirWellnessCoefficient.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
