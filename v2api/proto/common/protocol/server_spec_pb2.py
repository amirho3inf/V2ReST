# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: common/protocol/server_spec.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from common.net import address_pb2 as common_dot_net_dot_address__pb2
from common.protocol import user_pb2 as common_dot_protocol_dot_user__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='common/protocol/server_spec.proto',
  package='v2ray.core.common.protocol',
  syntax='proto3',
  serialized_options=b'\n\036com.v2ray.core.common.protocolP\001Z.github.com/v2fly/v2ray-core/v4/common/protocol\252\002\032V2Ray.Core.Common.Protocol',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n!common/protocol/server_spec.proto\x12\x1av2ray.core.common.protocol\x1a\x18\x63ommon/net/address.proto\x1a\x1a\x63ommon/protocol/user.proto\"\x82\x01\n\x0eServerEndpoint\x12\x32\n\x07\x61\x64\x64ress\x18\x01 \x01(\x0b\x32!.v2ray.core.common.net.IPOrDomain\x12\x0c\n\x04port\x18\x02 \x01(\r\x12.\n\x04user\x18\x03 \x03(\x0b\x32 .v2ray.core.common.protocol.UserBo\n\x1e\x63om.v2ray.core.common.protocolP\x01Z.github.com/v2fly/v2ray-core/v4/common/protocol\xaa\x02\x1aV2Ray.Core.Common.Protocolb\x06proto3'
  ,
  dependencies=[common_dot_net_dot_address__pb2.DESCRIPTOR,common_dot_protocol_dot_user__pb2.DESCRIPTOR,])




_SERVERENDPOINT = _descriptor.Descriptor(
  name='ServerEndpoint',
  full_name='v2ray.core.common.protocol.ServerEndpoint',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='address', full_name='v2ray.core.common.protocol.ServerEndpoint.address', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='port', full_name='v2ray.core.common.protocol.ServerEndpoint.port', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user', full_name='v2ray.core.common.protocol.ServerEndpoint.user', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=120,
  serialized_end=250,
)

_SERVERENDPOINT.fields_by_name['address'].message_type = common_dot_net_dot_address__pb2._IPORDOMAIN
_SERVERENDPOINT.fields_by_name['user'].message_type = common_dot_protocol_dot_user__pb2._USER
DESCRIPTOR.message_types_by_name['ServerEndpoint'] = _SERVERENDPOINT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ServerEndpoint = _reflection.GeneratedProtocolMessageType('ServerEndpoint', (_message.Message,), {
  'DESCRIPTOR' : _SERVERENDPOINT,
  '__module__' : 'common.protocol.server_spec_pb2'
  # @@protoc_insertion_point(class_scope:v2ray.core.common.protocol.ServerEndpoint)
  })
_sym_db.RegisterMessage(ServerEndpoint)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)