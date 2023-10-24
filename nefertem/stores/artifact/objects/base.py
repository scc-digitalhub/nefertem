"""
Abstract class for artifact store.
"""
from abc import ABCMeta, abstractmethod
from typing import Any

from pydantic import BaseModel

from nefertem.utils.logger import LOGGER
from nefertem.utils.uri_utils import rebuild_uri


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
    """Store URI."""

    is_default: bool = False
    """Determine if a Store is the default one."""

    config: dict | None = {}
    """Dictionary containing the configuration for the backend."""


class ArtifactStore(metaclass=ABCMeta):
    """
    Abstract artifact class that defines methods to persist/fetch
    artifacts into/from different storage backends.

    Attributes
    ----------
    name : str
        Name of store.
    type : str
        Type of store, e.g. s3, sql, local.
    artifact_uri : str
        An URI string that points to the storage.
    temp_dir : str
        Temporary download path.
    config : dict, default = None
        A dictionary with the credentials/configurations for the backend storage.
    is_default : bool
        Flag to indicate if this is the default store.
    """

    def __init__(
        self,
        name: str,
        store_type: str,
        uri: str,
        temp_dir: str,
        is_default: bool,
    ) -> None:
        """
        Constructor.
        """
        self.name = name
        self.store_type = store_type
        self.uri = uri
        self.temp_dir = temp_dir
        self.is_default = is_default

        # Path registry
        self._cache = {}

        # Logger
        self.logger = LOGGER

    @abstractmethod
    def persist_artifact(self, src: Any, dst: str, src_name: str, metadata: dict) -> None:
        """
        Method to persist an artifact.
        """

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

    def get_run_path(self, exp_name: str, run_id: str) -> str:
        """
        Return the path of the artifact store for the Run.
        """
        return rebuild_uri(self.uri, exp_name, run_id)

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
