"""
Dummy metadata store module.
"""
from nefertem.stores.metadata.objects.base import MetadataStore


class DummyMetadataStore(MetadataStore):
    """
    Dummy metadata store object implementation.

    Only allows the client to interact with store methods.
    """

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

    def get_run_metadata_uri(self, *args) -> None:
        """
        Placeholder method.

        Returns
        -------
        None
        """
