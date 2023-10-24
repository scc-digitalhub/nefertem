"""
PolarsDataFrameDuckDBReader module.
"""
from __future__ import annotations

import typing

import duckdb

from nefertem.readers.base.native import NativeReader
from nefertem.utils.exceptions import StoreError

if typing.TYPE_CHECKING:
    import polars as pl


class PolarsDataFrameDuckDBReader(NativeReader):
    """
    PolarsDataFrameDuckDBReader class.

    It allows to read a resource as polars DataFrame.
    """

    def fetch_data(self, src: str, query: str) -> pl.DataFrame:
        """
        Fetch resource from backend.
        """
        return self._read_df_from_db(src, query)

    @staticmethod
    def _read_df_from_db(src: str, query: str) -> pl.DataFrame:
        """
        Use polars to read data from db.
        """
        try:
            # Not thread safe apparently, do not use this.
            conn = duckdb.connect(database=src, read_only=True)
            return conn.sql(query).pl()
        except Exception as ex:
            raise StoreError(f"Unable to read data from query: {query}. Arguments: {str(ex.args)}")
