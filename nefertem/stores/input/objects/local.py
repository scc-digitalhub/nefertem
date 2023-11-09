"""
LocalInputStore module.
"""

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

    def fetch_file(self, src: str) -> str:
        """
        Return the path where a resource it is stored.

        Parameters
        ----------
        src : str
            The name of the file.

        Returns
        -------
        str
            The location of the requested file.
        """
        return src

    def fetch_native(self, src: str) -> str:
        """
        Return a native format path for a resource.

        Parameters
        ----------
        src : str
            The name of the file.

        Returns
        -------
        str
            The location of the requested file.
        """
        return src
