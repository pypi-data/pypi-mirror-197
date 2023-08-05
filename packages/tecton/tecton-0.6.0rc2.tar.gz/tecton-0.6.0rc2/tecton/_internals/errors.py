from typing import Iterable
from typing import List
from typing import Set

from tecton._internals.utils import KEY_DELETION_MAX
from tecton_core.errors import TectonInternalError
from tecton_core.errors import TectonValidationError

# Generic
INTERNAL_ERROR = lambda message: TectonInternalError(
    f"We seem to have encountered an error. Please contact support for assistance. Error details: {message}"
)
MDS_INACCESSIBLE = lambda host_port: TectonInternalError(
    f"Failed to connect to Tecton at {host_port}, please check your connectivity or contact support"
)
VALIDATION_ERROR_FROM_MDS = lambda message, trace_id: TectonValidationError(f"{message}, trace ID: {trace_id}")

INTERNAL_ERROR_FROM_MDS = lambda message, trace_id: TectonInternalError(
    f"Internal Tecton server error, please contact support with error details: {message}, trace ID: {trace_id}"
)

INVALID_SPINE_TYPE = lambda t: TectonValidationError(
    f"Invalid type of spine '{t}'. Spine must be an instance of [pyspark.sql.dataframe.DataFrame, " "pandas.DataFrame]."
)
UNSUPPORTED_OPERATION = lambda op, reason: TectonValidationError(f"Operation '{op}' is not supported: {reason}")
INVALID_SPINE_TIME_KEY_TYPE_SPARK = lambda t: TectonValidationError(
    f"Invalid type of timestamp_key column in the given spine. Expected TimestampType, got {t}"
)
INVALID_SPINE_TIME_KEY_TYPE_PANDAS = lambda t: TectonValidationError(
    f"Invalid type of timestamp_key column in the given spine. Expected datetime, got {t}"
)
MISSING_SPINE_COLUMN = lambda param, col, existing_cols: TectonValidationError(
    f"{param} column is missing from the spine. Expected to find '{col}' among available spine columns: '{', '.join(existing_cols)}'."
)
MISSING_REQUEST_DATA_IN_SPINE = lambda key, existing_cols: TectonValidationError(
    f"Request context key '{key}' not found in spine schema. Expected to find '{key}' among available spine columns: '{', '.join(existing_cols)}'."
)
NONEXISTENT_WORKSPACE = lambda name, workspaces: TectonValidationError(
    f'Workspace "{name}" not found. Available workspaces: {workspaces}'
)
INCORRECT_MATERIALIZATION_ENABLED_FLAG = lambda user_set_bool, server_side_bool: TectonValidationError(
    f"'is_live={user_set_bool}' argument does not match the value on the server: {server_side_bool}"
)
UNSUPPORTED_OPERATION_IN_DEVELOPMENT_WORKSPACE = lambda op: TectonValidationError(
    f"Operation '{op}' is not supported in a development workspace"
)
INVALID_JOIN_KEYS_TYPE = lambda t: TectonValidationError(
    f"Invalid type for join_keys. Expected Dict[str, Union[int, str, bytes]], got {t}"
)
INVALID_REQUEST_DATA_TYPE = lambda t: TectonValidationError(
    f"Invalid type for request_data. Expected Dict[str, Union[int, str, bytes, float]], got {t}"
)
INVALID_REQUEST_CONTEXT_TYPE = lambda t: TectonValidationError(
    f"Invalid type for request_context_map. Expected Dict[str, Union[int, str, bytes, float]], got {t}"
)
FV_NEEDS_TO_BE_BATCH_TRIGGER_MANUAL = lambda fv_name: TectonValidationError(
    f"batch_trigger of Feature View {fv_name} needs to be BatchTriggerType.MANUAL"
)


def INVALID_INDIVIDUAL_JOIN_KEY_TYPE(key: str, type_str: str):
    return TectonValidationError(
        f"Invalid type for join_key '{key}'. Expected either type int, str, or bytes, got {type_str}"
    )


def EMPTY_ARGUMENT(argument: str):
    return TectonValidationError(f"Argument '{argument}' can not be empty.")


def EMPTY_ELEMENT_IN_ARGUMENT(argument: str):
    return TectonValidationError(f"Argument '{argument}' can not have an empty element.")


def DUPLICATED_ELEMENTS_IN_ARGUMENT(argument: str):
    return TectonValidationError(f"Argument '{argument}' can not have duplicated elements.")


def DATA_SOURCE_HAS_NO_BATCH_CONFIG(data_source: str):
    return TectonValidationError(
        f"Cannot run get_dataframe on Data Source '{data_source}' because it does not have a batch_config"
    )


def FEATURE_VIEW_HAS_NO_BATCH_SOURCE(feature_view: str):
    return TectonValidationError(
        f"Cannot run get_historical_features with from_source=True for Feature View {feature_view} because it depends on a Data Source which does not have a batch config set. Please retry with from_source=False"
    )


def FEATURE_VIEW_HAS_NO_STREAM_SOURCE(feature_view: str):
    return TectonValidationError(
        f"Cannot run run_stream on Feature View {feature_view} because it does not have a Stream Source"
    )


def UNKNOWN_REQUEST_CONTEXT_KEY(keys, key):
    return TectonValidationError(f"Unknown request context key '{key}', expected one of: {keys}")


FV_TIME_KEY_MISSING = lambda fv_name: TectonValidationError(
    f"Argument 'timestamp_key' is required for the feature definition '{fv_name}'"
)
FV_NO_MATERIALIZED_DATA = lambda fv_name: TectonValidationError(
    f"Feature definition '{fv_name}' doesn't have any materialized data. "
    "Materialization jobs may not have updated the offline feature store yet. "
    "Please monitor using materialization_status() or use from_source=True to compute from source data."
)

FV_NOT_SUPPORTED_PREVIEW = TectonValidationError(
    "This method cannot be used with this type of Feature Definition. Please use get_historical_features(spine=spine)."
)
FD_PREVIEW_NO_MATERIALIZED_OFFLINE_DATA = TectonValidationError(
    f"No materialized offline data found. If this Feature Definition was recently created,"
    + " its materialization backfill may still be in progress. This can be monitored using materialization_status()."
    + " In the meantime, you can set use_materialized_data=False on preview() to compute features directly from data sources."
)
FV_GET_FEATURE_DF_NO_SPINE = TectonValidationError("get_feature_dataframe() requires a 'spine' argument.")


ODFV_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE = lambda odfv_name, workspace: TectonValidationError(
    f"On-Demand Feature View {odfv_name} is in workspace {workspace}, which is a development workspace (does not have materialization enabled). "
    "Please use from_source=True when retrieving features or alternatively use a live workspace and configure offline materialization for all dependent Feature Views."
)

FD_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE = lambda fd_name, workspace: TectonValidationError(
    f"Feature Definition {fd_name} is in workspace {workspace}, which is a development workspace (does not have materialization enabled). "
    "Please use from_source=True when getting features (not applicable for Feature Tables) or "
    "alternatively configure offline materialization for this Feature Definition in a live workspace."
)

FEATURE_TABLE_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE = lambda ft_name, workspace: TectonValidationError(
    f"Feature Table {ft_name} is in workspace {workspace}, which is a development workspace (does not have materialization enabled). "
    "Please apply this Feature Table to a live workspace and ingest some features before using with get_historical_features()."
)

FEATURE_TABLE_GET_ONLINE_FEATURES_FROM_DEVELOPMENT_WORKSPACE = lambda ft_name, workspace: TectonValidationError(
    f"Feature Table {ft_name} is in workspace {workspace}, which is a development workspace (does not have materialization enabled). "
    "Please apply this Feature Table to a live workspace and ingest some features before using with get_online_features()."
)

FEATURE_TABLE_GET_MATERIALIZED_FEATURES_OFFLINE_FALSE = lambda ft_name: TectonValidationError(
    f"Feature Table {ft_name} does not have offline materialization enabled, i.e. offline=True. Cannot retrieve offline feature if offline materializaiton is not enabled."
)

FD_GET_MATERIALIZED_FEATURES_FROM_LOCAL_OBJECT = lambda fv_name, fco_name: TectonValidationError(
    f"{fco_name} {fv_name} is defined locally, i.e. it has not been applied to a Tecton workspace. "
    "In order to force fetching data from the Offline store (i.e. from_source=False) this Feature View must be applied to a Live workspace and have materialization enabled (i.e. offline=True)."
)

FD_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE_GFD = lambda fv_name, workspace: TectonValidationError(
    f"Feature View {fv_name} is in workspace {workspace}, which is a development workspace (does not have materialization enabled). "
    "In order to force fetching data from the Offline store (i.e. from_source=False) this Feature View must be applied to a Live workspace and have materialization enabled (i.e. offline=True)."
)

FV_WITH_INC_BACKFILLS_GET_MATERIALIZED_FEATURES_FROM_DEVELOPMENT_WORKSPACE = lambda fv_name, workspace: TectonValidationError(
    f"Feature view {fv_name} uses incremental backfills and is in workspace {workspace}, which is a development workspace (does not have materialization enabled). "
    + "Computing features from source is not supported for Batch Feature Views with incremental_backfills set to True. "
    + "Enable offline materialization for this feature view in a live workspace to use `get_historical_features()`, or use `run()` to test this feature view without materializing data."
)

FV_WITH_INC_BACKFILLS_GET_MATERIALIZED_FEATURES_IN_LOCAL_MODE = lambda fv_name: TectonValidationError(
    f"Feature view {fv_name} uses incremental backfills and is locally defined which means materialization is not enabled."
    + "Computing features from source is not supported for Batch Feature Views with incremental_backfills set to True. "
    + "Apply and enable offline materialization for this feature view in a live workspace to use `get_historical_features()`, or use `run()` to test this feature view locally in a notebook."
)

FD_GET_FEATURES_MATERIALIZATION_DISABLED = lambda fd_name: TectonValidationError(
    f"Feature View {fd_name} does not have offline materialization turned on. "
    "In order to force fetching data from the Offline store (i.e. from_source=False) this Feature View must be applied to a Live workspace and have materialization enabled (i.e. offline=True)."
)

FV_GET_FEATURES_MATERIALIZATION_DISABLED_GFD = lambda fv_name: TectonValidationError(
    f"Feature View {fv_name} does not have offline materialization turned on. "
    f"Try calling this function with 'use_materialized_data=False' "
    "or alternatively configure offline materialization for this Feature View."
)


# DataSources
DS_STREAM_PREVIEW_ON_NON_STREAM = TectonValidationError("'start_stream_preview' called on non-streaming data source")

DS_DATAFRAME_NO_TIMESTAMP = TectonValidationError(
    "Cannot find timestamp column for this data source. Please call 'get_dataframe' without parameters 'start_time' or 'end_time'."
)

DS_RAW_DATAFRAME_NO_TIMESTAMP_FILTER = TectonValidationError(
    "The method 'get_dataframe()' cannot filter on timestamps when 'apply_translator' is False. "
    "'start_time' and 'end_time' must be None."
)

DS_INCORRECT_SUPPORTS_TIME_FILTERING = TectonValidationError(
    "Cannot filter on timestamps when supports_time_filtering on data source is False. "
    "'start_time' and 'end_time' must be None."
)


def FS_SPINE_JOIN_KEY_OVERRIDE_INVALID(spine_key, fv_key, possible_columns):
    return TectonValidationError(
        f"Spine join key '{spine_key}' (mapped from FeatureView join key '{fv_key}') not found in spine schema {possible_columns}"
    )


def FS_SPINE_TIMESTAMP_KEY_INVALID(timestamp_key, possible_columns):
    return TectonValidationError(f"Spine timestamp key '{timestamp_key}' not found in spine schema {possible_columns}")


def FS_BACKEND_ERROR(message):
    return TectonInternalError(f"Error calling Feature Service API: {message}")


FS_GET_FEATURE_VECTOR_REQUIRED_ARGS = TectonValidationError(
    "get_feature_vector requires at least one of join_keys or request_context_map"
)

FS_API_KEY_MISSING = TectonValidationError(
    "API key is required for online feature requests, but was not found in the environment. Please generate a key and set TECTON_API_KEY "
    + "using https://docs.tecton.ai/v2/examples/fetch-real-time-features.html#generating-an-api-key"
)

# Entity
def FV_INVALID_MOCK_SOURCES(mock_sources_keys: Iterable[str], fn_param: Iterable[str]):
    mock_sources_keys = mock_sources_keys if mock_sources_keys else set()
    return TectonValidationError(
        f"Mock sources' keys {mock_sources_keys} do not match FeatureView's parameters {fn_param}"
    )


def FV_INVALID_MOCK_INPUTS(mock_inputs: Set[str], inputs: Set[str]):
    input_names = str(mock_inputs) if mock_inputs else "{}"
    return TectonValidationError(f"Mock input names {input_names} do not match FeatureView's inputs {inputs}")


def FV_INVALID_MOCK_INPUTS_NUM_ROWS(num_rows: List[int]):
    return TectonValidationError(
        f"Number of rows are not equal across all mock_inputs. Number of rows found are: {str(num_rows)}."
    )


def FV_INVALID_MOCK_INPUT_SCHEMA(input_name: str, mock_columns: Set[str], expected_columns: Set[str]):
    return TectonValidationError(
        f"mock_inputs['{input_name}'] has mismatch schema columns {mock_columns}, expected {expected_columns}"
    )


def FV_UNSUPPORTED_ARG(invalid_arg_name: str):
    return TectonValidationError(f"Argument '{invalid_arg_name}' is not supported for this FeatureView type.")


def FV_INVALID_ARG_VALUE(arg_name: str, value: str, expected: str):
    return TectonValidationError(f"Invalid argument value '{arg_name}={value}', supported value(s): '{expected}'")


def FV_INVALID_ARG_COMBO(arg_names: List[str]):
    return TectonValidationError(f"Invalid argument combinations; {str(arg_names)} cannot be used together.")


FT_UNABLE_TO_ACCESS_SOURCE_DATA = lambda fv_name: TectonValidationError(
    f"The source data for FeatureTable {fv_name} does not exist. "
    "Please use from_source=False when calling this function."
)


class InvalidTransformationMode(TectonValidationError):
    def __init__(self, name: str, got: str, allowed_modes: List[str]):
        super().__init__(f"Transformation mode for '{name}' got '{got}', must be one of: {', '.join(allowed_modes)}")


class InvalidConstantType(TectonValidationError):
    def __init__(self, value, allowed_types):
        allowed_types = [str(allowed_type) for allowed_type in allowed_types]
        super().__init__(
            f"Tecton const value '{value}' must have one of the following types: {', '.join(allowed_types)}"
        )


class InvalidTransformInvocation(TectonValidationError):
    def __init__(self, transformation_name: str, got: str):
        super().__init__(
            f"Allowed arguments for Transformation '{transformation_name}' are: "
            f"tecton.const, tecton.materialization_context, transformations, and DataSource inputs. Got: '{got}'"
        )


# Dataset
DATASET_SPINE_COLUMNS_NOT_SET = TectonValidationError(
    "Cannot retrieve spine DF when Dataset was created without a spine."
)

# Feature Retrevial
def GET_HISTORICAL_FEATURES_WRONG_PARAMS(params: List[str], if_statement: str):
    return TectonValidationError("Cannot provide parameters " + ", ".join(params) + f" if {if_statement}")


GET_ONLINE_FEATURES_REQUIRED_ARGS = TectonValidationError(
    "get_online_features requires at least one of join_keys or request_data to be set."
)

GET_ONLINE_FEATURES_ODFV_JOIN_KEYS = TectonValidationError(
    "get_online_features requires the 'join_keys' argument for this On-Demand Feature View since it has other Feature Views as inputs"
)

GET_ONLINE_FEATURES_FS_JOIN_KEYS = TectonValidationError(
    "get_online_features requires the 'join_keys' argument for this Feature Service"
)

GET_FEATURE_VECTOR_FS_JOIN_KEYS = TectonValidationError(
    "get_feature_vector requires the 'join_keys' argument for this Feature Service"
)

FS_GET_ONLINE_FEATURES_REQUIRED_ARGS = TectonValidationError(
    "get_online_features requires at least one of join_keys or request_data"
)


def GET_ONLINE_FEATURES_MISSING_REQUEST_KEY(keys: Set[str]):
    return TectonValidationError(f"The following required keys are missing in request_data: " + ", ".join(keys))


def GET_FEATURE_VECTOR_MISSING_REQUEST_KEY(keys: Set[str]):
    return TectonValidationError(f"The following required keys are missing in request_context_map: " + ", ".join(keys))


def GET_ONLINE_FEATURES_FS_NO_REQUEST_DATA(keys: List[str]):
    return TectonValidationError(
        "get_online_features requires the 'request_data' argument for this Feature Service since it contains an On-Demand Feature View. "
        + "Expected the following request data keys: "
        + ", ".join(keys)
    )


def GET_FEATURE_VECTOR_FS_NO_REQUEST_DATA(keys: List[str]):
    return TectonValidationError(
        "get_feature_vector requires the 'request_context_map' argument for this Feature Service since it contains an On-Demand Feature View. "
        + "Expected the following request context keys: "
        + ", ".join(keys)
    )


def GET_ONLINE_FEATURES_FV_NO_REQUEST_DATA(keys: List[str]):
    return TectonValidationError(
        "get_online_features requires the 'request_data' argument for On-Demand Feature Views. Expected the following request context keys: "
        + ", ".join(keys)
    )


def GET_FEATURE_VECTOR_FV_NO_REQUEST_DATA(keys: List[str]):
    return TectonValidationError(
        "get_feature_vector requires the 'request_context_map' argument for On-Demand Feature Views. Expected the following request context keys: "
        + ", ".join(keys)
    )


ODFV_WITH_FT_INPUT_DEV_WORKSPACE = lambda ft_name: TectonValidationError(
    f"This On-Demand Feature View has a Feature Table, {ft_name}, as an input. Feature Table feature retrieval cannot be used in a dev workspace. Please apply the Feature Table to a live workspace to retrieve features."
)

ODFV_WITH_FT_INPUT_LOCAL_MODE = lambda ft_name: TectonValidationError(
    f"This On-Demand Feature View has a Feature Table, {ft_name}, as an input. Feature Table feature retrieval cannot be used when the Feature Table is locally defined. Please apply the Feature Table to a live workspace to retrieve features."
)

ODFV_WITH_FT_INPUT_FROM_SOURCE = lambda ft_name: TectonValidationError(
    f"This On-Demand Feature View has a Feature Table, {ft_name}, as an input. Feature Table features must be retrieved from the offline store, i.e. with from_source=False."
)

ODFV_WITH_UNMATERIALIZED_FV_INPUT_FROM_SOURCE_FALSE = lambda fv_name: TectonValidationError(
    f"This On-Demand Feature View has a Feature View, {fv_name}, as an input, which does not have materialization enabled (offline=False). Either retrieve features with from_source=True (not applicable for Feature Tables) or enable offline materialization for the input feature views."
)

LOCAL_ODFV_WITH_DEV_WORKSPACE_FV_INPUT_FROM_SOURCE_FALSE = lambda fv_name: TectonValidationError(
    f"This On-Demand Feature View has a Feature View, {fv_name}, as an input, which belongs to a dev workspace and therefore does not have materialization enabled. Either retrieve features with from_source=True (not applicable for Feature Tables) or apply this Feature View to a live workspace with offline=True."
)

LOCAL_ODFV_WITH_LOCAL_FV_INPUT_FROM_SOURCE_FALSE = lambda fv_name: TectonValidationError(
    f"This On-Demand Feature View has a Feature View, {fv_name}, as an input, that is locally defined and therefore does not have materialization enabled. Either retrieve features with from_source=True or apply this Feature View to a live workspace with offline=True."
)

FROM_SOURCE_WITH_FT = TectonValidationError(
    f"Computing features from source is not supported for Feature Tables. Try calling this method with from_source=False."
)

USE_MATERIALIZED_DATA_WITH_FT = TectonValidationError(
    f"Computing features from source is not supported for Feature Tables. Try calling this method with use_materialized_data=True."
)


FS_WITH_FT_DEVELOPMENT_WORKSPACE = TectonValidationError(
    f"This Feature Service contains a Feature Table and fetching historical features for Feature Tables is not supported in a development workspace. This method is only supported in live workspaces."
)


FV_WITH_FT_DEVELOPMENT_WORKSPACE = TectonValidationError(
    f"This Feature View has a Feature Table input and fetching historical features for Feature Tables is not supported in a development workspace. This method is only supported in live workspaces."
)


# Backfill Config Validation
BFC_MODE_SINGLE_REQUIRED_FEATURE_END_TIME_WHEN_START_TIME_SET = TectonValidationError(
    "feature_end_time is required when feature_start_time is set, for a FeatureView with "
    + "single_batch_schedule_interval_per_job backfill mode."
)

BFC_MODE_SINGLE_INVALID_FEATURE_TIME_RANGE = TectonValidationError(
    "Run with single_batch_schedule_interval_per_job backfill mode only supports time range equal to batch_schedule"
)

INCORRECT_KEYS = lambda keys, join_keys: TectonValidationError(
    f"Requested keys to be deleted ({keys}) do not match the expected join keys ({join_keys})."
)

NO_STORE_SELECTED = TectonValidationError(f"One of online or offline store must be selected.")

TOO_MANY_KEYS = TectonValidationError(f"Max number of keys to be deleted is {KEY_DELETION_MAX}.")

OFFLINE_STORE_NOT_SUPPORTED = TectonValidationError(
    "Only DeltaLake is supported for entity deletion in offline feature stores."
)

FV_UNSUPPORTED_AGGREGATION = TectonValidationError(
    f"Argument 'aggregation_level' is not supported for Feature Views with `aggregations` not specified."
)
INVALID_JOIN_KEY_TYPE = lambda t: TectonValidationError(
    f"Invalid type of join keys '{t}'. Keys must be an instance of [pyspark.sql.dataframe.DataFrame, "
    "pandas.DataFrame]."
)
DUPLICATED_COLS_IN_KEYS = lambda t: TectonValidationError(f"Argument keys {t} have duplicated column names. ")

MISSING_SNOWFAKE_CONNECTION_REQUIREMENTS = lambda param: TectonValidationError(
    f"Snowflake connection is missing the variable {param}. Please ensure the following parameters are set when creating your snowflake connection:  database, warehouse, and schema. "
)

ATHENA_COMPUTE_ONLY_SUPPORTED_IN_LIVE_WORKSPACE = TectonValidationError(
    "Athena compute can only be used in live workspaces. Current workspace is not live. Please unset ALPHA_ATHENA_COMPUTE_ENABLED or switch to a live workspace."
)

ATHENA_COMPUTE_NOT_SUPPORTED_IN_LOCAL_MODE = TectonValidationError(
    "Athena compute can only be used in on applied Tecton objects in live workspaces. Using a locally definied Tecton object is not currently supported with Athena."
)

# Notebook Development
def TECTON_OBJECT_REQUIRES_VALIDATION(function_name: str, class_name: str, fco_name: str):
    return TectonValidationError(
        f"{class_name} '{fco_name}' must be validated before `{function_name}` can be called. Call `validate()` to validate this object. If you'd like to enable automatic validation, you can use `tecton.set_validation_mode('auto')` or set the environment variable `TECTON_VALIDATION_MODE=auto`. Note that validation requires connected compute (Spark/Snowflake/etc.) and makes requests to your Tecton instance's API."
    )


def RUN_REQUIRES_VALIDATION(function_name: str, class_name: str, fco_name: str):
    return TectonValidationError(
        f"{class_name} '{fco_name}' must be validated before `{function_name}` can be called. If you'd like to skip validation (e.g. for unit testing), use `test_run()` instead. In order to run validations either call `validate()` or enable automatic validation, you can use `tecton.set_validation_mode('auto')` or set the environment variable `TECTON_VALIDATION_MODE=auto`. Note that validation requires connected compute (Spark/Snowflake/etc.) and makes requests to your Tecton instance's API."
    )


def INVALID_USAGE_FOR_LOCAL_TECTON_OBJECT(function_name: str):
    return TectonValidationError(
        f"`{function_name}` can only be called on Tecton objects that have been applied to a Tecton workspace. This object was defined locally."
    )


def INVALID_USAGE_FOR_REMOTE_TECTON_OBJECT(function_name: str):
    return TectonValidationError(
        f"`{function_name}` can only be called on Tecton objects that have been defined locally. This object was retrieved from a Tecton workspace."
    )


def INVALID_USAGE_FOR_LOCAL_FEATURE_TABLE_OBJECT(function_name: str):
    return TectonValidationError(
        f"`{function_name}` can only be called on Feature Tables that have been applied to a Tecton workspace. This object was defined locally, which means this Feature Table cannot be materialized. Feature Tables require materialization in order to ingest features and perform feature retrieval."
    )


def CANNOT_USE_LOCAL_RUN_ON_REMOTE_OBJECT(function_name: str):
    return TectonValidationError(
        f"`{function_name}` can only be called on locally defined Tecton objects. This object was retrieved from a Tecton workpace. Please use `run()` instead."
    )


def INVALID_NUMBER_OF_FEATURE_VIEW_INPUTS(num_sources: int, num_inputs: int):
    return TectonValidationError(
        f"Number of Feature View Inputs ({num_inputs}) should match the number of Data Sources ({num_sources}) in the definition."
    )


BUILD_ARGS_INTERNAL_ERROR = TectonInternalError(
    "_build_args() is for internal use only and can only be called on local objects"
)


UNSUPPORTED_FRAMEWORK_VERSION = RuntimeError(
    "The existing feature definitions have been applied with an older SDK. Please downgrade the Tecton SDK or upgrade the feature definitions."
)
