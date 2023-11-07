"""
FileReader module.
"""
from nefertem.readers._base import DataReader


class FileReader(DataReader):
    """
    FileReader class.

    The FileReader object tells the stores to fetch physical
    resources from backend and store them locally.
    """

    def fetch_data(self, src: str) -> str:
        """
        Fetch resource from backend.
        """
        return self.store.fetch_file(src)
