# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from ..monitoring import MonitoredEntity_pb2 as monitoring_dot_MonitoredEntity__pb2
from ..monitoring import MonitoredModel_pb2 as monitoring_dot_MonitoredModel__pb2


class MonitoredModelServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.createMonitoredModel = channel.unary_unary(
        '/ai.verta.monitoring.MonitoredModelService/createMonitoredModel',
        request_serializer=monitoring_dot_MonitoredModel__pb2.CreateMonitoredModel.SerializeToString,
        response_deserializer=monitoring_dot_MonitoredModel__pb2.MonitoredModel.FromString,
        )
    self.updateMonitoredModel = channel.unary_unary(
        '/ai.verta.monitoring.MonitoredModelService/updateMonitoredModel',
        request_serializer=monitoring_dot_MonitoredModel__pb2.UpdateMonitoredModel.SerializeToString,
        response_deserializer=monitoring_dot_MonitoredModel__pb2.MonitoredModel.FromString,
        )
    self.findMonitoredModel = channel.unary_unary(
        '/ai.verta.monitoring.MonitoredModelService/findMonitoredModel',
        request_serializer=monitoring_dot_MonitoredModel__pb2.FindMonitoredModels.SerializeToString,
        response_deserializer=monitoring_dot_MonitoredModel__pb2.FindMonitoredModels.Response.FromString,
        )
    self.deleteMonitoredModel = channel.unary_unary(
        '/ai.verta.monitoring.MonitoredModelService/deleteMonitoredModel',
        request_serializer=monitoring_dot_MonitoredModel__pb2.DeleteMonitoredModel.SerializeToString,
        response_deserializer=monitoring_dot_MonitoredEntity__pb2.Empty.FromString,
        )


class MonitoredModelServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def createMonitoredModel(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def updateMonitoredModel(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def findMonitoredModel(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def deleteMonitoredModel(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_MonitoredModelServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'createMonitoredModel': grpc.unary_unary_rpc_method_handler(
          servicer.createMonitoredModel,
          request_deserializer=monitoring_dot_MonitoredModel__pb2.CreateMonitoredModel.FromString,
          response_serializer=monitoring_dot_MonitoredModel__pb2.MonitoredModel.SerializeToString,
      ),
      'updateMonitoredModel': grpc.unary_unary_rpc_method_handler(
          servicer.updateMonitoredModel,
          request_deserializer=monitoring_dot_MonitoredModel__pb2.UpdateMonitoredModel.FromString,
          response_serializer=monitoring_dot_MonitoredModel__pb2.MonitoredModel.SerializeToString,
      ),
      'findMonitoredModel': grpc.unary_unary_rpc_method_handler(
          servicer.findMonitoredModel,
          request_deserializer=monitoring_dot_MonitoredModel__pb2.FindMonitoredModels.FromString,
          response_serializer=monitoring_dot_MonitoredModel__pb2.FindMonitoredModels.Response.SerializeToString,
      ),
      'deleteMonitoredModel': grpc.unary_unary_rpc_method_handler(
          servicer.deleteMonitoredModel,
          request_deserializer=monitoring_dot_MonitoredModel__pb2.DeleteMonitoredModel.FromString,
          response_serializer=monitoring_dot_MonitoredEntity__pb2.Empty.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ai.verta.monitoring.MonitoredModelService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
