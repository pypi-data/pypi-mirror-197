# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/data/tecton_api_key.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tecton_proto.auth import principal_pb2 as tecton__proto_dot_auth_dot_principal__pb2
from tecton_proto.common import id_pb2 as tecton__proto_dot_common_dot_id__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&tecton_proto/data/tecton_api_key.proto\x12\x11tecton_proto.data\x1a!tecton_proto/auth/principal.proto\x1a\x1ctecton_proto/common/id.proto\"\xe0\x02\n\x0cTectonApiKey\x12\'\n\x02id\x18\x01 \x01(\x0b\x32\x17.tecton_proto.common.IdR\x02id\x12\x1d\n\nhashed_key\x18\x02 \x01(\tR\thashedKey\x12 \n\x0b\x64\x65scription\x18\x03 \x01(\tR\x0b\x64\x65scription\x12\x1a\n\x08\x61rchived\x18\x04 \x01(\x08R\x08\x61rchived\x12\x1d\n\ncreated_by\x18\x05 \x01(\tR\tcreatedBy\x12!\n\x0cobscured_key\x18\x06 \x01(\tR\x0bobscuredKey\x12\x19\n\x08is_admin\x18\x07 \x01(\x08R\x07isAdmin\x12\x12\n\x04name\x18\x08 \x01(\tR\x04name\x12!\n\tis_active\x18\t \x01(\x08:\x04trueR\x08isActive\x12\x36\n\x07\x63reator\x18\n \x01(\x0b\x32\x1c.tecton_proto.auth.PrincipalR\x07\x63reatorB\x13\n\x0f\x63om.tecton.dataP\x01')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.data.tecton_api_key_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\017com.tecton.dataP\001'
  _TECTONAPIKEY._serialized_start=127
  _TECTONAPIKEY._serialized_end=479
# @@protoc_insertion_point(module_scope)
