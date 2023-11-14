"""
PandasDataFrameDuckDBReader module.
"""
from typing import Any

import duckdb
import pandas as pd
from nefertem_validation_duckdb.utils import describe_resource

from nefertem.readers.objects._base import DataReader
from nefertem.utils.exceptions import StoreError
from nefertem.utils.utils import listify


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

    def fetch_local_data(self, srcs: list[str]) -> pd.DataFrame:
        """
        Fetch resource from backend.
        """
        dfs = []
        for src in srcs:
            path = self.store.fetch_file(src)
            res = describe_resource(path)
            dfs.append(self._read_df_from_path(res))
        return pd.concat(dfs)

    def _read_df_from_path(self, resource: dict) -> pd.DataFrame:
        """
        Read a file into a pandas DataFrame.
        """
        paths = listify(resource.get("path"))
        file_format = resource.get("format")

        if file_format == "csv":
            csv_args = {
                "sep": resource.get("dialect", {}).get("csv", {}).get("delimiter", ","),
                "encoding": resource.get("encoding"),
            }
            list_df = [pd.read_csv(i, **csv_args) for i in paths]
        elif file_format in ["xls", "xlsx", "ods", "odf"]:
            list_df = [pd.read_excel(i) for i in paths]
        elif file_format == "parquet":
            list_df = [pd.read_parquet(i) for i in paths]
        else:
            raise ValueError("File extension not supported!")

        return pd.concat(list_df)
