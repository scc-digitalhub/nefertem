"""
Abstract class for artifact store.
"""
from abc import ABCMeta, abstractmethod

from pydantic import BaseModel

from nefertem.utils.logger import LOGGER


class StoreConfig(BaseModel):
    """
    Store configuration class.
    It defines the configuration settings for a Store like endpoints, credentials, etc.
    It is modelled on different kind of Store.
    """


class StoreParameters(BaseModel):
    """
    Store configuration class.
    """

    name: str
    """Store id."""

    uri: str
    """Store uri."""

    config: dict | None = {}
    """Dictionary containing the configuration for the backend."""


class InputStore(metaclass=ABCMeta):
    """
    Abstract class that defines methods to fetch artifacts from different storage backends.

    Attributes
    ----------
    name : str
        Name of store.
    type : str
        Type of store, e.g. s3, sql, local.
    temp_dir : str
        Temporary download path.
    config : dict, default = None
        A dictionary with the credentials/configurations for the backend storage.
    """

    def __init__(self, name: str, uri: str, store_type: str, temp_dir: str) -> None:
        """
        Constructor.
        """
        self.name = name
        self.uri = uri
        self.store_type = store_type
        self.temp_dir = temp_dir

        # Path registry
        self._cache = {}

        # Logger
        self.logger = LOGGER

    ############################
    # Read methods
    ############################

    @abstractmethod
    def fetch_file(self, src: str) -> str:
        """
        Return the temporary path where a resource it is stored.
        """

    @abstractmethod
    def fetch_native(self, src: str) -> str:
        """
        Return a native format path for a resource.
        """

    ############################
    # Cache methods
    ############################

    def _get_resource(self, key: str) -> str | None:
        """
        Method to return temporary path of a registered resource.
        """
        return self._cache.get(key)

    def _register_resource(self, key: str, path: str) -> None:
        """
        Method to register a resource into the path registry.
        """
        if key not in self._cache:
            self._cache[key] = path

    def clean_paths(self) -> None:
        """
        Delete all temporary paths references from stores.
        """
        self._cache = {}
