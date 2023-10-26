"""
PandasDataFrameDuckDBReader module.
"""
from __future__ import annotations

import typing
from typing import Any

import duckdb

from nefertem.readers.base import DataReader
from nefertem.utils.exceptions import StoreError

if typing.TYPE_CHECKING:
    import pandas as pd


class PandasDataFrameDuckDBReader(DataReader):
    """
    PandasDataFrameDuckDBReader class.

    It allows to read a resource as pandas DataFrame.
    """

    def fetch_data(self, src: str, query: str) -> pd.DataFrame:
        """
        Fetch resource from backend.
        """
        return self._read_df_from_db(src, query)

    @staticmethod
    def _read_df_from_db(src: str, query: str) -> pd.DataFrame:
        """
        Use the pandas to read data from db.
        """
        try:
            conn = duckdb.connect(database=src, read_only=True)
            conn.execute(query)
            return conn.fetchdf()
        except Exception as ex:
            raise StoreError(f"Unable to read data from query: {query}. Arguments: {str(ex.args)}")

    @staticmethod
    def return_head(df: pd.DataFrame) -> dict:
        """
        Return head(100) of DataFrame as dict.
        """
        return df.head(100).to_dict()

    @staticmethod
    def return_first_value(df: pd.DataFrame) -> Any:
        """
        Return first value of DataFrame.
        """
        return df.iloc[0, 0]

    @staticmethod
    def return_length(df: pd.DataFrame) -> int:
        """
        Return length of DataFrame.
        """
        return df.shape[0]
