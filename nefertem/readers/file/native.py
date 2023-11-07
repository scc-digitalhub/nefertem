"""
NativeReader module.
"""
from nefertem.readers._base import DataReader


class NativeReader(DataReader):
    """
    NativeReader class.

    The NativeReader object tells the stores to return
    a string reference to a resource according to store type,
    e.g. a connection string for SQL store or an encoded URL
    for remote storages.
    """

    def fetch_data(self, src: str) -> str:
        """
        Fetch resource from backend.
        """
        return self.store.fetch_native(src)
