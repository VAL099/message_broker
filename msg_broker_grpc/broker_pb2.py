# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: broker.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0c\x62roker.proto\x12\nmsg_broker\"4\n\x12MessageWithContent\x12\r\n\x05topic\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\t\"\x19\n\x06Reply1\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x1e\n\rRequestUpdate\x12\r\n\x05topic\x18\x01 \x01(\t\"\x1e\n\x0bPublication\x12\x0f\n\x07\x63ontent\x18\x01 \x01(\t\"\x1f\n\x0eRequestHistory\x12\r\n\x05topic\x18\x01 \x01(\t\"\x1a\n\x07History\x12\x0f\n\x07\x63ontent\x18\x01 \x01(\t2\xe8\x01\n\x0fhandle_messages\x12\x44\n\x0eGetPublication\x12\x1e.msg_broker.MessageWithContent\x1a\x12.msg_broker.Reply1\x12J\n\x14\x42roadcastPublication\x12\x19.msg_broker.RequestUpdate\x1a\x17.msg_broker.Publication\x12\x43\n\x0eHistoryHandler\x12\x1a.msg_broker.RequestHistory\x1a\x13.msg_broker.History0\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'broker_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MESSAGEWITHCONTENT._serialized_start=28
  _MESSAGEWITHCONTENT._serialized_end=80
  _REPLY1._serialized_start=82
  _REPLY1._serialized_end=107
  _REQUESTUPDATE._serialized_start=109
  _REQUESTUPDATE._serialized_end=139
  _PUBLICATION._serialized_start=141
  _PUBLICATION._serialized_end=171
  _REQUESTHISTORY._serialized_start=173
  _REQUESTHISTORY._serialized_end=204
  _HISTORY._serialized_start=206
  _HISTORY._serialized_end=232
  _HANDLE_MESSAGES._serialized_start=235
  _HANDLE_MESSAGES._serialized_end=467
# @@protoc_insertion_point(module_scope)
