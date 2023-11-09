"""
Module for common terms definition.
"""

# Nefertem version
NEFERTEM_VERSION: str = "2.0.0"

# Data readers type
BASE_FILE_READER: str = "FileReader"
BASE_NATIVE_READER: str = "NativeReader"
PANDAS_DATAFRAME_FILE_READER: str = "PandasDataFrameFileReader"
PANDAS_DATAFRAME_DUCKDB_READER: str = "PandasDataFrameDuckDBReader"
PANDAS_DATAFRAME_SQL_READER: str = "PandasDataFrameSQLReader"
POLARS_DATAFRAME_FILE_READER: str = "PolarsDataFrameFileReader"
POLARS_DATAFRAME_DUCKDB_READER: str = "PolarsDataFrameDuckDBReader"
POLARS_DATAFRAME_SQL_READER: str = "PolarsDataFrameSQLReader"

# Generics
DUMMY: str = "_dummy"
DEFAULT_DIRECTORY: str = "./ntruns/tmp"
DEFAULT_EXPERIMENT: str = "exp"
