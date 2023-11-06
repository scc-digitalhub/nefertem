"""
Dummy artifact store module.
"""
from nefertem.stores.input.objects.base import InputStore, StoreConfig


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
        uri: str,
        store_type: str,
        temp_dir: str,
        config: dict,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(name, uri, store_type, temp_dir)
        self.config = config

    def persist_artifact(self, *args) -> None:
        """
        Placeholder methods.

        Returns
        -------
        None
        """

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