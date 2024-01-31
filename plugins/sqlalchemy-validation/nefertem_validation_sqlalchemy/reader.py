"""
PandasDataFrameReader module.
"""
from __future__ import annotations

import pandas as pd
from nefertem_core.readers.objects._base import DataReader
from nefertem_core.utils.exceptions import StoreError
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


class PandasDataFrameSQLReader(DataReader):
    """
    PandasDataFrameSQLReader class.

    It allows to read a resource as pandas DataFrame.
    """

    def fetch_data(self, src: str, query: str) -> pd.DataFrame:
        """
        Fetch resource from backend.
        """
        conn_string = self.store.fetch_native(src)
        return self._read_df_from_db(conn_string, query)

    @staticmethod
    def _get_engine(conn_str: str) -> Engine:
        """
        Create a SQLAlchemy Engine.
        """
        try:
            return create_engine(conn_str)
        except Exception as ex:
            raise StoreError(f"Something wrong with connection string. Arguments: {str(ex.args)}")

    def _read_df_from_db(self, conn_str: str, query: str) -> pd.DataFrame:
        """
        Use the pandas to read data from db.
        """
        engine = self._get_engine(conn_str)
        try:
            return pd.read_sql(query, engine)
        except Exception as ex:
            raise StoreError(f"Unable to read data from query: {query}. Arguments: {str(ex.args)}")
        finally:
            engine.dispose()
