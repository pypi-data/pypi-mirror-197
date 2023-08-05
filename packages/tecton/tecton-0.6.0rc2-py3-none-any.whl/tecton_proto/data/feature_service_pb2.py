# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/data/feature_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tecton_proto.validation import validator_pb2 as tecton__proto_dot_validation_dot_validator__pb2
from tecton_proto.common import column_type_pb2 as tecton__proto_dot_common_dot_column__type__pb2
from tecton_proto.common import data_type_pb2 as tecton__proto_dot_common_dot_data__type__pb2
from tecton_proto.args import feature_service_pb2 as tecton__proto_dot_args_dot_feature__service__pb2
from tecton_proto.data import fco_metadata_pb2 as tecton__proto_dot_data_dot_fco__metadata__pb2
from tecton_proto.common import id_pb2 as tecton__proto_dot_common_dot_id__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'tecton_proto/data/feature_service.proto\x12\x11tecton_proto.data\x1a\'tecton_proto/validation/validator.proto\x1a%tecton_proto/common/column_type.proto\x1a#tecton_proto/common/data_type.proto\x1a\'tecton_proto/args/feature_service.proto\x1a$tecton_proto/data/fco_metadata.proto\x1a\x1ctecton_proto/common/id.proto\"\xe9\x03\n\x0e\x46\x65\x61tureService\x12\x45\n\x12\x66\x65\x61ture_service_id\x18\x01 \x01(\x0b\x32\x17.tecton_proto.common.IdR\x10\x66\x65\x61tureServiceId\x12M\n\x11\x66\x65\x61ture_set_items\x18\x02 \x03(\x0b\x32!.tecton_proto.data.FeatureSetItemR\x0f\x66\x65\x61tureSetItems\x12\x41\n\x0c\x66\x63o_metadata\x18\t \x01(\x0b\x32\x1e.tecton_proto.data.FcoMetadataR\x0b\x66\x63oMetadata\x12\x34\n\x16online_serving_enabled\x18\x0b \x01(\x08R\x14onlineServingEnabled\x12>\n\x07logging\x18\x0c \x01(\x0b\x32$.tecton_proto.args.LoggingConfigArgsR\x07logging\x12^\n\x0fvalidation_args\x18\r \x01(\x0b\x32\x35.tecton_proto.validation.FeatureServiceValidationArgsR\x0evalidationArgsJ\x04\x08\x03\x10\x04J\x04\x08\x04\x10\x05J\x04\x08\x05\x10\x06J\x04\x08\x06\x10\x07J\x04\x08\x07\x10\x08J\x04\x08\x08\x10\tJ\x04\x08\n\x10\x0b\"\x86\x02\n\x10JoinKeyComponent\x12*\n\x11spine_column_name\x18\x01 \x01(\tR\x0fspineColumnName\x12H\n\x0c\x62inding_type\x18\x02 \x01(\x0e\x32%.tecton_proto.data.JoinKeyBindingTypeR\x0b\x62indingType\x12@\n\x0b\x63olumn_type\x18\x03 \x01(\x0e\x32\x1f.tecton_proto.common.ColumnTypeR\ncolumnType\x12:\n\tdata_type\x18\x04 \x01(\x0b\x32\x1d.tecton_proto.common.DataTypeR\x08\x64\x61taType\"V\n\x0fJoinKeyTemplate\x12\x43\n\ncomponents\x18\x01 \x03(\x0b\x32#.tecton_proto.data.JoinKeyComponentR\ncomponents\"\x8a\x02\n\x0e\x46\x65\x61tureSetItem\x12?\n\x0f\x66\x65\x61ture_view_id\x18\x06 \x01(\x0b\x32\x17.tecton_proto.common.IdR\rfeatureViewId\x12\x62\n\x18join_configuration_items\x18\x03 \x03(\x0b\x32(.tecton_proto.data.JoinConfigurationItemR\x16joinConfigurationItems\x12\x1c\n\tnamespace\x18\x04 \x01(\tR\tnamespace\x12\'\n\x0f\x66\x65\x61ture_columns\x18\x05 \x03(\tR\x0e\x66\x65\x61tureColumnsJ\x04\x08\x01\x10\x02J\x06\x08\xe8\x07\x10\xe9\x07\"s\n\x15JoinConfigurationItem\x12*\n\x11spine_column_name\x18\x01 \x01(\tR\x0fspineColumnName\x12.\n\x13package_column_name\x18\x02 \x01(\tR\x11packageColumnName*|\n\x12JoinKeyBindingType\x12!\n\x1dJOIN_KEY_BINDING_TYPE_UNKNOWN\x10\x00\x12\x1f\n\x1bJOIN_KEY_BINDING_TYPE_BOUND\x10\x01\x12\"\n\x1eJOIN_KEY_BINDING_TYPE_WILDCARD\x10\x02\x42\x13\n\x0f\x63om.tecton.dataP\x01')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.data.feature_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\017com.tecton.dataP\001'
  _JOINKEYBINDINGTYPE._serialized_start=1519
  _JOINKEYBINDINGTYPE._serialized_end=1643
  _FEATURESERVICE._serialized_start=289
  _FEATURESERVICE._serialized_end=778
  _JOINKEYCOMPONENT._serialized_start=781
  _JOINKEYCOMPONENT._serialized_end=1043
  _JOINKEYTEMPLATE._serialized_start=1045
  _JOINKEYTEMPLATE._serialized_end=1131
  _FEATURESETITEM._serialized_start=1134
  _FEATURESETITEM._serialized_end=1400
  _JOINCONFIGURATIONITEM._serialized_start=1402
  _JOINCONFIGURATIONITEM._serialized_end=1517
# @@protoc_insertion_point(module_scope)
