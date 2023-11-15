"""
FileReader module.
"""
from __future__ import annotations

from pathlib import Path

from nefertem.readers.objects._base import DataReader


class FileReader(DataReader):
    """
    FileReader class.

    The FileReader invokes stores fetch_file method to fetch the resource from the backend
    and returns the path to the downloaded resource.
    """

    def fetch_data(self, src: str) -> Path:
        """
        Fetch resource from backend.

        Parameters
        ----------
        src : str
            Resource path.

        Returns
        -------
        Path
            Path to the downloaded resource.
        """
        return self.store.fetch_file(src)
