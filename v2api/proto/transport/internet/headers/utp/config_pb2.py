# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: transport/internet/headers/utp/config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='transport/internet/headers/utp/config.proto',
  package='v2ray.core.transport.internet.headers.utp',
  syntax='proto3',
  serialized_options=b'\n-com.v2ray.core.transport.internet.headers.utpP\001Z=github.com/v2fly/v2ray-core/v4/transport/internet/headers/utp\252\002)V2Ray.Core.Transport.Internet.Headers.Utp',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n+transport/internet/headers/utp/config.proto\x12)v2ray.core.transport.internet.headers.utp\"\x19\n\x06\x43onfig\x12\x0f\n\x07version\x18\x01 \x01(\rB\x9c\x01\n-com.v2ray.core.transport.internet.headers.utpP\x01Z=github.com/v2fly/v2ray-core/v4/transport/internet/headers/utp\xaa\x02)V2Ray.Core.Transport.Internet.Headers.Utpb\x06proto3'
)




_CONFIG = _descriptor.Descriptor(
  name='Config',
  full_name='v2ray.core.transport.internet.headers.utp.Config',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='v2ray.core.transport.internet.headers.utp.Config.version', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=90,
  serialized_end=115,
)

DESCRIPTOR.message_types_by_name['Config'] = _CONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Config = _reflection.GeneratedProtocolMessageType('Config', (_message.Message,), {
  'DESCRIPTOR' : _CONFIG,
  '__module__' : 'transport.internet.headers.utp.config_pb2'
  # @@protoc_insertion_point(class_scope:v2ray.core.transport.internet.headers.utp.Config)
  })
_sym_db.RegisterMessage(Config)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)