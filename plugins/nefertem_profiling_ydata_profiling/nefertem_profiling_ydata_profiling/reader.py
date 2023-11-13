"""
PandasDataFrameReader module.
"""
import pandas as pd

from nefertem.readers.objects._base import DataReader
from nefertem_profiling_ydata_profiling.utils import describe_resource
from nefertem.utils.utils import listify


class PandasDataFrameFileReader(DataReader):
    """
    PandasDataFrameFileReader class.

    Read a DataFrame from local file.
    """

    def fetch_data(self, src: str) -> pd.DataFrame:
        """
        Fetch resource from backend.
        """
        path = self.store.fetch_file(src)
        res = describe_resource(path)
        return self._read_df_from_path(res)

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
