"""
DataReader registry.
"""

# Base imports
from nefertem.utils.commons import (
    BASE_FILE_READER,
    BASE_NATIVE_READER,
    PANDAS_DATAFRAME_DUCKDB_READER,
    PANDAS_DATAFRAME_FILE_READER,
    PANDAS_DATAFRAME_SQL_READER,
    POLARS_DATAFRAME_DUCKDB_READER,
    POLARS_DATAFRAME_FILE_READER,
    POLARS_DATAFRAME_SQL_READER,
)

# Registry of data readers
REGISTRY = {
    BASE_FILE_READER: ["nefertem.readers.file.file", "FileReader"],
    BASE_NATIVE_READER: ["nefertem.readers.file.native", "NativeReader"],
    PANDAS_DATAFRAME_DUCKDB_READER: [
        "nefertem.readers.pandas.duckdb",
        "PandasDataFrameDuckDBReader",
    ],
    PANDAS_DATAFRAME_FILE_READER: [
        "nefertem.readers.pandas.file",
        "PandasDataFrameFileReader",
    ],
    PANDAS_DATAFRAME_SQL_READER: [
        "nefertem.readers.pandas.sql",
        "PandasDataFrameSQLReader",
    ],
    POLARS_DATAFRAME_DUCKDB_READER: [
        "nefertem.readers.polars.duckdb",
        "PolarsDataFrameDuckDBReader",
    ],
    POLARS_DATAFRAME_FILE_READER: [
        "nefertem.readers.polars.file",
        "PolarsDataFrameFileReader",
    ],
    POLARS_DATAFRAME_SQL_READER: [
        "nefertem.readers.polars.sql",
        "PolarsDataFrameSQLReader",
    ],
}
