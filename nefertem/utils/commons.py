"""
Module for common terms definition.
"""
from typing import List


# Nefertem version
NEFERTEM_VERSION: str = ""


# Libraries
LIBRARY_FRICTIONLESS: str = "frictionless"
LIBRARY_PANDAS_PROFILING: str = "pandas_profiling"
LIBRARY_YDATA_PROFILING: str = "ydata_profiling"
LIBRARY_DUCKDB: str = "duckdb"
LIBRARY_SQLALCHEMY: str = "sqlalchemy"
LIBRARY_GREAT_EXPECTATIONS: str = "great_expectations"
LIBRARY_DUMMY: str = "_dummy"
LIBRARY_EVIDENTLY: str = "evidently"

# Data readers format
DATAREADER_FILE: str = "file"
DATAREADER_NATIVE: str = "native"
DATAREADER_BUFFER: str = "buffer"


# Data readers type
BASE_FILE_READER: str = "FileReader"
BASE_NATIVE_READER: str = "NativeReader"
BASE_BUFFER_READER: str = "BufferReader"
PANDAS_DATAFRAME_FILE_READER: str = "PandasDataFrameFileReader"
PANDAS_DATAFRAME_DUCKDB_READER: str = "PandasDataFrameDuckDBReader"
PANDAS_DATAFRAME_SQL_READER: str = "PandasDataFrameSQLReader"
POLARS_DATAFRAME_FILE_READER: str = "PolarsDataFrameFileReader"
POLARS_DATAFRAME_DUCKDB_READER: str = "PolarsDataFrameDuckDBReader"
POLARS_DATAFRAME_SQL_READER: str = "PolarsDataFrameSQLReader"


# Store types
STORE_DUMMY: str = "_dummy"
STORE_LOCAL: str = "local"
STORE_HTTP: str = "http"
STORE_FTP: str = "ftp"
STORE_S3: str = "s3"
STORE_AZURE: str = "azure"
STORE_SQL: str = "sql"
STORE_ODBC: str = "odbc"


# Schemes
SCHEME_LOCAL: List[str] = [
    "",
    "file",
]
SCHEME_HTTP: List[str] = [
    "http",
    "https",
]
SCHEME_S3: List[str] = [
    "s3",
]
SCHEME_AZURE: List[str] = [
    "wasb",
    "wasbs",
]
SCHEME_FTP: List[str] = [
    "ftp",
]
SCHEME_SQL: List[str] = [
    "sql",
    "postgresql",
    "mysql",
    "mssql",
    "oracle",
    "sqlite",
]
SCHEME_ODBC: List[str] = [
    "dremio",
    "odbc",
]
SCHEME_DUCKDB: List[str] = [
    "duckdb",
]
SCHEME_DUMMY: List[str] = [
    "_dummy",
]


# Constraints

# Frictionless
CONSTRAINT_FRICTIONLESS_SCHEMA: str = "frictionless_schema"

# SQL constraints expectation
CONSTRAINT_SQL_EMPTY: str = "empty"
CONSTRAINT_SQL_NON_EMPTY: str = "non-empty"
CONSTRAINT_SQL_EXACT: str = "exact"
CONSTRAINT_SQL_RANGE: str = "range"
CONSTRAINT_SQL_MINIMUM: str = "minimum"
CONSTRAINT_SQL_MAXIMUM: str = "maximum"

#  SQL constraint dats to check
CONSTRAINT_SQL_CHECK_VALUE: str = "value"
CONSTRAINT_SQL_CHECK_ROWS: str = "rows"


# API endpoints
API_BASE: str = "/api/project/"
API_RUN_METADATA: str = "/run-metadata"
API_DJ_REPORT: str = "/short-report"
API_DJ_SCHEMA: str = "/short-schema"
API_DJ_PROFILE: str = "/data-profile"
API_ARTIFACT_METADATA: str = "/artifact-metadata"
API_RUN_ENV: str = "/run-environment"


# Filenames metadata
FN_RUN_METADATA: str = "run_metadata.json"
FN_DJ_REPORT: str = "report_{}.json"
FN_DJ_SCHEMA: str = "schema_{}.json"
FN_DJ_PROFILE: str = "profile_{}.json"
FN_ARTIFACT_METADATA: str = "artifact_metadata_{}.json"
FN_RUN_ENV: str = "run_env.json"


# Metadata type
MT_RUN_METADATA: str = "run"
MT_DJ_REPORT: str = "report"
MT_DJ_SCHEMA: str = "schema"
MT_DJ_PROFILE: str = "profile"
MT_ARTIFACT_METADATA: str = "artifact"
MT_RUN_ENV: str = "run_env"


# Execution operations
OPERATION_INFERENCE: str = "inference"
OPERATION_PROFILING: str = "profiling"
OPERATION_VALIDATION: str = "validation"


# Result typology
RESULT_WRAPPED: str = "wrapped"
RESULT_NEFERTEM: str = "nefertem"
RESULT_RENDERED: str = "rendered"
RESULT_LIBRARY: str = "library"


# Execution status
STATUS_INIT: str = "created"
STATUS_RUNNING: str = "executing"
STATUS_INTERRUPTED: str = "interrupdted"
STATUS_FINISHED: str = "finished"
STATUS_ERROR: str = "error"


# Generics
GENERIC_DUMMY: str = "_dummy"
DEFAULT_DIRECTORY: str = "./ntruns/tmp"
DEFAULT_PROJECT: str = "project"
DEFAULT_EXPERIMENT: str = "experiment"
