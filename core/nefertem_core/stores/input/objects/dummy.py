"""
Dummy artifact store module.
"""
from __future__ import annotations

from nefertem_core.stores.input.objects._base import InputStore, StoreConfig


class DummyStoreConfig(StoreConfig):
    """
    Dummy store configuration.
    """


class DummyInputStore(InputStore):
    """
    Dummy artifact store object implementation.

    Only allows the client to interact store methods.
    """

    def __init__(
        self,
        name: str,
        store_type: str,
        temp_dir: str,
        config: DummyStoreConfig,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(name, store_type, temp_dir)
        self.config = config

    ############################
    # Read methods
    ############################

    def fetch_file(self, *args) -> None:
        """
        Placeholder methods.

        Returns
        -------
        None
        """

    def fetch_native(self, *args) -> None:
        """
        Placeholder methods.

        Returns
        -------
        None
        """
