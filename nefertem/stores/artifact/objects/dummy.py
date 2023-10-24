"""
Dummy artifact store module.
"""
from nefertem.stores.artifact.objects.base import ArtifactStore, StoreConfig


class DummyStoreConfig(StoreConfig):
    """
    Dummy store configuration.
    """


class DummyArtifactStore(ArtifactStore):
    """
    Dummy artifact store object implementation.

    Only allows the client to interact store methods.
    """

    def __init__(
        self,
        name: str,
        store_type: str,
        uri: str,
        temp_dir: str,
        is_default: bool,
        config: dict,
    ) -> None:
        """
        Constructor.
        """
        super().__init__(name, store_type, uri, temp_dir, is_default)
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
