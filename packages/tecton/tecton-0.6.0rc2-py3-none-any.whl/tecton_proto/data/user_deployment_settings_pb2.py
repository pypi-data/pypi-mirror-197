# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/data/user_deployment_settings.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tecton_proto.common import secret_pb2 as tecton__proto_dot_common_dot_secret__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n0tecton_proto/data/user_deployment_settings.proto\x12\x11tecton_proto.data\x1a tecton_proto/common/secret.proto\"\xfa\x02\n\x16UserDeploymentSettings\x12G\n user_deployment_settings_version\x18\x01 \x01(\x05R\x1duserDeploymentSettingsVersion\x12R\n\x11\x64\x61tabricks_config\x18\x02 \x01(\x0b\x32#.tecton_proto.data.DatabricksConfigH\x00R\x10\x64\x61tabricksConfig\x12T\n\x13user_spark_settings\x18\x03 \x01(\x0b\x32$.tecton_proto.data.UserSparkSettingsR\x11userSparkSettings\x12O\n\x0ftenant_settings\x18\x05 \x01(\x0b\x32&.tecton_proto.data.TenantSettingsProtoR\x0etenantSettingsB\x16\n\x14\x64\x61ta_platform_configJ\x04\x08\x04\x10\x05\"\xdf\x01\n\x10\x44\x61tabricksConfig\x12#\n\rworkspace_url\x18\x01 \x01(\tR\x0cworkspaceUrl\x12\x38\n\tapi_token\x18\x02 \x01(\x0b\x32\x1b.tecton_proto.common.SecretR\x08\x61piToken\x12\x1b\n\tuser_name\x18\x03 \x01(\tR\x08userName\x12*\n\x11user_display_name\x18\x04 \x01(\tR\x0fuserDisplayName\x12#\n\rspark_version\x18\x05 \x01(\tR\x0csparkVersion\"\xd7\x01\n\x11UserSparkSettings\x12\x30\n\x14instance_profile_arn\x18\x01 \x01(\tR\x12instanceProfileArn\x12R\n\nspark_conf\x18\x02 \x03(\x0b\x32\x33.tecton_proto.data.UserSparkSettings.SparkConfEntryR\tsparkConf\x1a<\n\x0eSparkConfEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\"\x94\x06\n\x13TenantSettingsProto\x12M\n\x14\x63hronosphere_api_key\x18\x01 \x01(\x0b\x32\x1b.tecton_proto.common.SecretR\x12\x63hronosphereApiKey\x12I\n!chronosphere_restrict_label_value\x18\x04 \x01(\tR\x1e\x63hronosphereRestrictLabelValue\x12M\n pseudonymize_amplitude_user_name\x18\x02 \x01(\x08:\x04trueR\x1dpseudonymizeAmplitudeUserName\x12T\n\'enable_user_editing_deployment_settings\x18\x03 \x01(\x08R#enableUserEditingDeploymentSettings\x12-\n\x13okta_admin_group_id\x18\x05 \x01(\tR\x10oktaAdminGroupId\x12+\n\x12okta_user_group_id\x18\x06 \x01(\tR\x0foktaUserGroupId\x12\x39\n\x19\x62\x61se_metadata_service_url\x18\x07 \x01(\tR\x16\x62\x61seMetadataServiceUrl\x12\x37\n\x18\x62\x61se_feature_service_url\x18\x08 \x01(\tR\x15\x62\x61seFeatureServiceUrl\x12:\n\x19spicedb_organization_name\x18\t \x01(\tR\x17spicedbOrganizationName\x12=\n\x1b\x63ustomer_facing_tenant_name\x18\n \x01(\tR\x18\x63ustomerFacingTenantName\x12\x41\n\x0c\x61ws_settings\x18\x0b \x01(\x0b\x32\x1e.tecton_proto.data.AwsSettingsR\x0b\x61wsSettings\x12\x30\n\x14internal_tenant_name\x18\x0c \x01(\tR\x12internalTenantName\"\xa8\x05\n\x0b\x41wsSettings\x12>\n\x0b\x64ynamo_role\x18\x06 \x01(\x0b\x32\x1d.tecton_proto.data.AwsIamRoleR\ndynamoRole\x12_\n\x11\x64ynamo_extra_tags\x18\x08 \x03(\x0b\x32\x33.tecton_proto.data.AwsSettings.DynamoExtraTagsEntryR\x0f\x64ynamoExtraTags\x12\x62\n\x12\x63ompute_extra_tags\x18\t \x03(\x0b\x32\x34.tecton_proto.data.AwsSettings.ComputeExtraTagsEntryR\x10\x63omputeExtraTags\x12\x41\n\x0c\x65mr_settings\x18\x0c \x01(\x0b\x32\x1e.tecton_proto.data.EmrSettingsR\x0b\x65mrSettings\x12Q\n\x12\x64ynamo_table_names\x18\r \x01(\x0b\x32#.tecton_proto.data.DynamoTableNamesR\x10\x64ynamoTableNames\x12]\n\x16object_store_locations\x18\x0e \x01(\x0b\x32\'.tecton_proto.data.ObjectStoreLocationsR\x14objectStoreLocations\x1a\x42\n\x14\x44ynamoExtraTagsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x1a\x43\n\x15\x43omputeExtraTagsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01J\x04\x08\x01\x10\x06J\x04\x08\x07\x10\x08J\x04\x08\n\x10\x0bJ\x04\x08\x0b\x10\x0c\"\x94\x01\n\nAwsIamRole\x12\x19\n\x08role_arn\x18\x01 \x01(\tR\x07roleArn\x12J\n\x11intermediate_role\x18\x02 \x01(\x0b\x32\x1d.tecton_proto.data.AwsIamRoleR\x10intermediateRole\x12\x1f\n\x0b\x65xternal_id\x18\x03 \x01(\tR\nexternalId\"S\n\nS3Location\x12\x12\n\x04path\x18\x01 \x01(\tR\x04path\x12\x31\n\x04role\x18\x02 \x01(\x0b\x32\x1d.tecton_proto.data.AwsIamRoleR\x04role\"\"\n\x0c\x44\x42\x46SLocation\x12\x12\n\x04path\x18\x01 \x01(\tR\x04path\"\xad\x01\n\x13ObjectStoreLocation\x12@\n\x0bs3_location\x18\x01 \x01(\x0b\x32\x1d.tecton_proto.data.S3LocationH\x00R\ns3Location\x12\x46\n\rdbfs_location\x18\x02 \x01(\x0b\x32\x1f.tecton_proto.data.DBFSLocationH\x00R\x0c\x64\x62\x66sLocationB\x0c\n\nstore_type\"V\n\x0b\x45mrSettings\x12G\n\x10\x65mr_control_role\x18\x01 \x01(\x0b\x32\x1d.tecton_proto.data.AwsIamRoleR\x0e\x65mrControlRole\"\xa8\x03\n\x10\x44ynamoTableNames\x12*\n\x11\x64\x61ta_table_prefix\x18\x01 \x01(\tR\x0f\x64\x61taTablePrefix\x12*\n\x11status_table_name\x18\x02 \x01(\tR\x0fstatusTableName\x12\x42\n\x1ejob_idempotence_key_table_name\x18\x03 \x01(\tR\x1ajobIdempotenceKeyTableName\x12*\n\x11\x63\x61nary_table_name\x18\x04 \x01(\tR\x0f\x63\x61naryTableName\x12/\n\x14\x64\x65lta_log_table_name\x18\x05 \x01(\tR\x11\x64\x65ltaLogTableName\x12.\n\x13metric_table_prefix\x18\x06 \x01(\tR\x11metricTablePrefix\x12\x34\n\x17\x64\x65lta_log_table_name_v2\x18\x07 \x01(\tR\x13\x64\x65ltaLogTableNameV2\x12\x35\n\x17job_metadata_table_name\x18\x08 \x01(\tR\x14jobMetadataTableName\"\xe0\x07\n\x14ObjectStoreLocations\x12P\n\x0fmaterialization\x18\x01 \x01(\x0b\x32&.tecton_proto.data.ObjectStoreLocationR\x0fmaterialization\x12Y\n\x14streaming_checkpoint\x18\x02 \x01(\x0b\x32&.tecton_proto.data.ObjectStoreLocationR\x13streamingCheckpoint\x12h\n\x1c\x66\x65\x61ture_server_configuration\x18\x03 \x01(\x0b\x32&.tecton_proto.data.ObjectStoreLocationR\x1a\x66\x65\x61tureServerConfiguration\x12I\n\x0c\x66\x65\x61ture_repo\x18\x04 \x01(\x0b\x32&.tecton_proto.data.ObjectStoreLocationR\x0b\x66\x65\x61tureRepo\x12G\n\x0b\x65mr_scripts\x18\x05 \x01(\x0b\x32&.tecton_proto.data.ObjectStoreLocationR\nemrScripts\x12]\n\x16materialization_params\x18\x06 \x01(\x0b\x32&.tecton_proto.data.ObjectStoreLocationR\x15materializationParams\x12S\n\x11intermediate_data\x18\x07 \x01(\x0b\x32&.tecton_proto.data.ObjectStoreLocationR\x10intermediateData\x12\\\n\x16\x66\x65\x61ture_server_logging\x18\x08 \x01(\x0b\x32&.tecton_proto.data.ObjectStoreLocationR\x14\x66\x65\x61tureServerLogging\x12\\\n\x16kafka_credentials_base\x18\t \x01(\x0b\x32&.tecton_proto.data.ObjectStoreLocationR\x14kafkaCredentialsBase\x12\\\n\x16push_api_configuration\x18\n \x01(\x0b\x32&.tecton_proto.data.ObjectStoreLocationR\x14pushApiConfiguration\x12O\n\x0f\x64\x61ta_validation\x18\x0b \x01(\x0b\x32&.tecton_proto.data.ObjectStoreLocationR\x0e\x64\x61taValidationB\x13\n\x0f\x63om.tecton.dataP\x01')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.data.user_deployment_settings_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\017com.tecton.dataP\001'
  _USERSPARKSETTINGS_SPARKCONFENTRY._options = None
  _USERSPARKSETTINGS_SPARKCONFENTRY._serialized_options = b'8\001'
  _AWSSETTINGS_DYNAMOEXTRATAGSENTRY._options = None
  _AWSSETTINGS_DYNAMOEXTRATAGSENTRY._serialized_options = b'8\001'
  _AWSSETTINGS_COMPUTEEXTRATAGSENTRY._options = None
  _AWSSETTINGS_COMPUTEEXTRATAGSENTRY._serialized_options = b'8\001'
  _USERDEPLOYMENTSETTINGS._serialized_start=106
  _USERDEPLOYMENTSETTINGS._serialized_end=484
  _DATABRICKSCONFIG._serialized_start=487
  _DATABRICKSCONFIG._serialized_end=710
  _USERSPARKSETTINGS._serialized_start=713
  _USERSPARKSETTINGS._serialized_end=928
  _USERSPARKSETTINGS_SPARKCONFENTRY._serialized_start=868
  _USERSPARKSETTINGS_SPARKCONFENTRY._serialized_end=928
  _TENANTSETTINGSPROTO._serialized_start=931
  _TENANTSETTINGSPROTO._serialized_end=1719
  _AWSSETTINGS._serialized_start=1722
  _AWSSETTINGS._serialized_end=2402
  _AWSSETTINGS_DYNAMOEXTRATAGSENTRY._serialized_start=2243
  _AWSSETTINGS_DYNAMOEXTRATAGSENTRY._serialized_end=2309
  _AWSSETTINGS_COMPUTEEXTRATAGSENTRY._serialized_start=2311
  _AWSSETTINGS_COMPUTEEXTRATAGSENTRY._serialized_end=2378
  _AWSIAMROLE._serialized_start=2405
  _AWSIAMROLE._serialized_end=2553
  _S3LOCATION._serialized_start=2555
  _S3LOCATION._serialized_end=2638
  _DBFSLOCATION._serialized_start=2640
  _DBFSLOCATION._serialized_end=2674
  _OBJECTSTORELOCATION._serialized_start=2677
  _OBJECTSTORELOCATION._serialized_end=2850
  _EMRSETTINGS._serialized_start=2852
  _EMRSETTINGS._serialized_end=2938
  _DYNAMOTABLENAMES._serialized_start=2941
  _DYNAMOTABLENAMES._serialized_end=3365
  _OBJECTSTORELOCATIONS._serialized_start=3368
  _OBJECTSTORELOCATIONS._serialized_end=4360
# @@protoc_insertion_point(module_scope)
