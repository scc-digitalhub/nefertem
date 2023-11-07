"""
PolarsDataFrameReader module.
"""
from pathlib import Path

import polars as pl

from nefertem.readers._base import DataReader
from nefertem.readers.utils import describe_resource
from nefertem.utils.utils import listify


class PolarsDataFrameFileReader(DataReader):
    """
    PolarsDataFrameFileReader class.

    Read a DataFrame from local file.
    """

    def fetch_data(self, src: str) -> pl.DataFrame:
        """
        Fetch resource from backend.
        """
        path = self.store.fetch_file(src)
        res = describe_resource(path)
        return self._read_df_from_path(res)

    def _read_df_from_path(self, resource: dict) -> pl.DataFrame:
        """
        Read a file into a Polars DataFrame.
        """
        paths = listify(resource.get("path"))
        file_format = resource.get("format")

        if file_format == "csv":
            csv_args = {
                "separator": resource.get("dialect", {}).get("delimiter", ","),
                "encoding": resource.get("encoding", "utf8"),
            }
            list_df = [pl.read_csv(Path(i), **csv_args) for i in paths]
        elif file_format == "parquet":
            list_df = [pl.read_parquet(Path(i)) for i in paths]
        else:
            raise ValueError("File extension not supported!")

        return pl.concat(list_df)

    def concat_data(self, dfs: list) -> pl.DataFrame:
        """
        Concatenate a list of Polars DataFrames.
        """
        return pl.concat(dfs)
