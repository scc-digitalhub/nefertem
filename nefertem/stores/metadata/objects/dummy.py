"""
Dummy metadata store module.
"""
from nefertem.stores.metadata.objects.base import MetadataStore


class DummyMetadataStore(MetadataStore):
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

    def _build_source_destination(self, *args) -> None:
        """
        Placeholder method.

        Returns
        -------
        None
        """

    def get_run_path(self, *args) -> None:
        """
        Placeholder method.

        Returns
        -------
        None
        """
