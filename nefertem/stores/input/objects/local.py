"""
LocalInputStore module.
"""
from __future__ import annotations

from pathlib import Path

from nefertem.stores.input.objects._base import InputStore, StoreConfig


class LocalStoreConfig(StoreConfig):
    """
    Local store configuration class.
    """


class LocalInputStore(InputStore):
    """
    Implementation of a local artifact store object that allows the user to
    interact with the local filesystem.
    """

    def __init__(self, name: str, store_type: str, temp_dir: str, config: LocalStoreConfig) -> None:
        """
        Constructor.
        """
        super().__init__(name, store_type, temp_dir)
        self.config = config

    ############################
    # Read methods
    ############################

    def fetch_file(self, src: str) -> Path:
        """
        Return the path where a resource it is stored.

        Parameters
        ----------
        src : str
            The name of the file.

        Returns
        -------
        Path
            The location of the requested file.
        """
        return Path(src)

    def fetch_native(self, src: str) -> Path:
        """
        Return a native format path for a resource.

        Parameters
        ----------
        src : str
            The name of the file.

        Returns
        -------
        Path
            The location of the requested file.
        """
        return Path(src)
