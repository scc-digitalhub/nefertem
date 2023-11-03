"""
Module for common terms definition.
"""

# Nefertem version
NEFERTEM_VERSION: str = "1.0.0"

# Mapper operations
RUN_OBJECT = "run"
RUN_HANDLER_OBJECT = "run_handler"


# Data readers type
BASE_FILE_READER: str = "FileReader"
BASE_NATIVE_READER: str = "NativeReader"
PANDAS_DATAFRAME_FILE_READER: str = "PandasDataFrameFileReader"
PANDAS_DATAFRAME_DUCKDB_READER: str = "PandasDataFrameDuckDBReader"
PANDAS_DATAFRAME_SQL_READER: str = "PandasDataFrameSQLReader"
POLARS_DATAFRAME_FILE_READER: str = "PolarsDataFrameFileReader"
POLARS_DATAFRAME_DUCKDB_READER: str = "PolarsDataFrameDuckDBReader"
POLARS_DATAFRAME_SQL_READER: str = "PolarsDataFrameSQLReader"

# Execution operations
INFER: str = "inference"
PROFILE: str = "profiling"
VALIDATE: str = "validation"


# Result typology
RESULT_ARTIFACT: str = "wrapped"
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
