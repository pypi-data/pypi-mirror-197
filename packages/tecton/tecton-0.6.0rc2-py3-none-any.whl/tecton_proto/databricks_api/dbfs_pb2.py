# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/databricks_api/dbfs.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&tecton_proto/databricks_api/dbfs.proto\x12\x1btecton_proto.databricks_api\"E\n\x11\x44\x62\x66sDeleteRequest\x12\x12\n\x04path\x18\x01 \x01(\tR\x04path\x12\x1c\n\trecursive\x18\x02 \x01(\x08R\trecursive\"*\n\x14\x44\x62\x66sGetStatusRequest\x12\x12\n\x04path\x18\x01 \x01(\tR\x04path\"U\n\x0f\x44\x62\x66sReadRequest\x12\x12\n\x04path\x18\x01 \x01(\tR\x04path\x12\x16\n\x06offset\x18\x02 \x01(\x03R\x06offset\x12\x16\n\x06length\x18\x03 \x01(\x03R\x06length\"E\n\x10\x44\x62\x66sReadResponse\x12\x1d\n\nbytes_read\x18\x01 \x01(\x03R\tbytesRead\x12\x12\n\x04\x64\x61ta\x18\x02 \x01(\x0cR\x04\x64\x61taB\x1d\n\x19\x63om.tecton.databricks_apiP\x01')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.databricks_api.dbfs_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\031com.tecton.databricks_apiP\001'
  _DBFSDELETEREQUEST._serialized_start=71
  _DBFSDELETEREQUEST._serialized_end=140
  _DBFSGETSTATUSREQUEST._serialized_start=142
  _DBFSGETSTATUSREQUEST._serialized_end=184
  _DBFSREADREQUEST._serialized_start=186
  _DBFSREADREQUEST._serialized_end=271
  _DBFSREADRESPONSE._serialized_start=273
  _DBFSREADRESPONSE._serialized_end=342
# @@protoc_insertion_point(module_scope)
