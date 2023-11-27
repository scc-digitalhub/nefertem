"""
Dummy metadata store module.
"""
from __future__ import annotations

from nefertem.stores.output.objects._base import OutputStore


class DummyOutputStore(OutputStore):
    """
    Dummy metadata store object implementation.

    Only allows the client to interact with store methods.
    """

    def __init__(self, path: str) -> None:
        super().__init__(path)

    def init_run(self, *args) -> None:
        """
        Placeholder method.

        Returns
        -------
        None
        """

    def log_metadata(self, *args) -> None:
        """
        Placeholder method.

        Returns
        -------
        None
        """

    def persist_artifact(self, *args) -> None:
        """
        Placeholder method.

        Returns
        -------
        None
        """
