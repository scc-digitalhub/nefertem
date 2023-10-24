"""
DataReader registry.
"""

# Base imports
from nefertem.readers.base.file import FileReader
from nefertem.readers.base.native import NativeReader
from nefertem.utils.commons import BASE_FILE_READER, BASE_NATIVE_READER

# Registry of data readers
REGISTRY = {
    BASE_FILE_READER: FileReader,
    BASE_NATIVE_READER: NativeReader,
}

try:
    from nefertem.readers.pandas.duckdb import PandasDataFrameDuckDBReader
    from nefertem.utils.commons import PANDAS_DATAFRAME_DUCKDB_READER

    REGISTRY[PANDAS_DATAFRAME_DUCKDB_READER] = PandasDataFrameDuckDBReader
except ImportError:
    ...

try:
    from nefertem.readers.pandas.file import PandasDataFrameFileReader
    from nefertem.utils.commons import PANDAS_DATAFRAME_FILE_READER

    REGISTRY[PANDAS_DATAFRAME_FILE_READER] = PandasDataFrameFileReader
except ImportError:
    ...

try:
    from nefertem.readers.pandas.sql import PandasDataFrameSQLReader
    from nefertem.utils.commons import PANDAS_DATAFRAME_SQL_READER

    REGISTRY[PANDAS_DATAFRAME_SQL_READER] = PandasDataFrameSQLReader
except ImportError:
    ...

try:
    from nefertem.readers.polars.duckdb import PolarsDataFrameDuckDBReader
    from nefertem.utils.commons import POLARS_DATAFRAME_DUCKDB_READER

    REGISTRY[POLARS_DATAFRAME_DUCKDB_READER] = PolarsDataFrameDuckDBReader
except ImportError:
    ...

try:
    from nefertem.readers.polars.file import PolarsDataFrameFileReader
    from nefertem.utils.commons import POLARS_DATAFRAME_FILE_READER

    REGISTRY[POLARS_DATAFRAME_FILE_READER] = PolarsDataFrameFileReader
except ImportError:
    ...

try:
    from nefertem.readers.polars.sql import PolarsDataFrameSQLReader
    from nefertem.utils.commons import POLARS_DATAFRAME_SQL_READER

    REGISTRY[POLARS_DATAFRAME_SQL_READER] = PolarsDataFrameSQLReader
except ImportError:
    ...
