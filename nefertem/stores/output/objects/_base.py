"""
Base abstract metadata store module.
"""
from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any


class OutputStore(metaclass=ABCMeta):
    """
    Abstract class that defines methods on how to persist metadata and artifacts into
    different storage backends.

    Attributes
    ----------
    path : str
        An URI string that points to the storage.

    """

    def __init__(self, path: str) -> None:
        self.path = path

    ############################
    # Run methods
    ############################

    @abstractmethod
    def init_run(self, exp_name: str, run_id: str, overwrite: bool) -> None:
        """
        Initial enviroment operation.
        """

    @abstractmethod
    def get_run_path(self) -> str:
        """
        Return run path.
        """

    ############################
    # Write methods
    ############################

    @abstractmethod
    def log_metadata(self, obj: dict, filename: str) -> None:
        """
        Method to log metadata.
        """

    @abstractmethod
    def persist_artifact(self, obj: Any, filename: str) -> None:
        """
        Method to persist an artifact.
        """
