"""
Base abstract metadata store module.
"""
from abc import ABCMeta, abstractmethod


class MetadataStore(metaclass=ABCMeta):
    """
    Abstract metadata class that defines methods on how to persist
    metadata into different storage backends.

    Attributes
    ----------
    name : str
        Name of store.
    type : str
        Type of store, e.g. http, local.
    path : str
        An URI string that points to the storage.
    config : dict, default = None
        A dictionary with the credentials/configurations
        for the backend storage.

    """

    def __init__(self, path: str) -> None:
        self.path = path

    @abstractmethod
    def init_run(self, exp_name: str, run_id: str, overwrite: bool) -> None:
        """
        Initial enviroment operation.
        """

    @abstractmethod
    def log_metadata(self, metadata: str, dst: str, src_type: str, overwrite: bool) -> None:
        """
        Method that log metadata.
        """

    @abstractmethod
    def get_run_path(self, exp_name: str, run_id: str) -> str:
        """
        Return the URI of the metadata store for the Run.
        """

    @abstractmethod
    def _build_source_destination(self, dst: str, src_type: str) -> str:
        """
        Return source destination based on source type.
        """
