# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: transport/internet/headers/wechat/config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='transport/internet/headers/wechat/config.proto',
  package='v2ray.core.transport.internet.headers.wechat',
  syntax='proto3',
  serialized_options=b'\n0com.v2ray.core.transport.internet.headers.wechatP\001Z@github.com/v2fly/v2ray-core/v4/transport/internet/headers/wechat\252\002,V2Ray.Core.Transport.Internet.Headers.Wechat',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n.transport/internet/headers/wechat/config.proto\x12,v2ray.core.transport.internet.headers.wechat\"\r\n\x0bVideoConfigB\xa5\x01\n0com.v2ray.core.transport.internet.headers.wechatP\x01Z@github.com/v2fly/v2ray-core/v4/transport/internet/headers/wechat\xaa\x02,V2Ray.Core.Transport.Internet.Headers.Wechatb\x06proto3'
)




_VIDEOCONFIG = _descriptor.Descriptor(
  name='VideoConfig',
  full_name='v2ray.core.transport.internet.headers.wechat.VideoConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=96,
  serialized_end=109,
)

DESCRIPTOR.message_types_by_name['VideoConfig'] = _VIDEOCONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

VideoConfig = _reflection.GeneratedProtocolMessageType('VideoConfig', (_message.Message,), {
  'DESCRIPTOR' : _VIDEOCONFIG,
  '__module__' : 'transport.internet.headers.wechat.config_pb2'
  # @@protoc_insertion_point(class_scope:v2ray.core.transport.internet.headers.wechat.VideoConfig)
  })
_sym_db.RegisterMessage(VideoConfig)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
