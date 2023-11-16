"""
Stores kinds module.
"""
from enum import Enum


class StoreKinds(Enum):
    """
    Enumerates the available store kinds.
    """

    DUMMY = "_dummy"
    LOCAL = "local"
    REMOTE = "remote"
    S3 = "s3"
    SQL = "sql"
