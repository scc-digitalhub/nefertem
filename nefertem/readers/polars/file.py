"""
PolarsDataFrameReader module.
"""
from __future__ import annotations

import typing
from pathlib import Path

from nefertem.plugins.utils.frictionless_utils import describe_resource
from nefertem.readers.base.file import FileReader
from nefertem.utils.utils import listify

if typing.TYPE_CHECKING:
    import polars as pl


class PolarsDataFrameFileReader(FileReader):
    """
    PolarsDataFrameFileReader class.

    Read a DataFrame from local file.
    """

    def fetch_data(self, src: str) -> pl.DataFrame:
        """
        Fetch resource from backend.
        """
        path = super().fetch_data(src)
        res = self._describe_resource(path)
        return self._read_df_from_path(res)

    def _describe_resource(self, src: str) -> dict:
        """
        Describe resource.
        """
        return describe_resource(src)

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