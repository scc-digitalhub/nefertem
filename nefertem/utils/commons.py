"""
Module for common terms definition.
"""

# Nefertem version
NEFERTEM_VERSION: str = "1.0.0"


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
DUMMY: str = "_dummy"
DEFAULT_DIRECTORY: str = "./ntruns/tmp"
DEFAULT_EXPERIMENT: str = "experiment"
