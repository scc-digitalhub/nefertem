"""
Stores kinds module.
"""
from enum import Enum


class StoreKinds(Enum):
    """
    Enumerates the available store kinds.
    """

    AZURE = "azure"
    DUMMY = "_dummy"
    FTP = "ftp"
    HTTP = "http"
    LOCAL = "local"
    ODBC = "odbc"
    S3 = "s3"
    SQL = "sql"


class SchemeKinds(Enum):
    """
    Enumerates the available scheme kinds.
    """

    AZURE = ["wasb", "wasbs"]
    DUCKDB = ["duckdb"]
    DUMMY = ["_dummy"]
    FTP = ["ftp"]
    HTTP = ["http", "https"]
    LOCAL = ["", "file"]
    ODBC = ["dremio", "odbc"]
    S3 = ["s3"]
    SQL = ["sql", "postgresql", "mysql", "mssql", "oracle", "sqlite"]
