"""
StoreHandler module.
"""
from __future__ import annotations

import typing

from nefertem.stores.builder import StoreBuilder
from nefertem.utils.commons import DEFAULT_DIRECTORY
from nefertem.utils.file_utils import clean_all

if typing.TYPE_CHECKING:
    from nefertem.stores.artifact.objects.base import ArtifactStore
    from nefertem.stores.metadata.objects.base import MetadataStore


class StoreHandler:
    """
    Handler layer between the Client interface, stores and factories.

    The StoreHandler contain a register that keeps track of stores.

    """

    def __init__(
        self,
        metadata_store: str | None = None,
        stores: list[dict] | None = None,
        tmp_dir: str | None = None,
    ) -> None:
        self._stores: dict[str, ArtifactStore] = {}
        self._md_store: MetadataStore = None
        self._default_store: ArtifactStore = None
        self._tmp_dir = tmp_dir if tmp_dir is not None else DEFAULT_DIRECTORY

        self._setup(metadata_store, stores)

    def _setup(self, path: str | None = None, configs: list[dict] | None = None) -> None:
        """
        Build stores according to configurations provided by user
        and register them into the store registry.
        """

        # Build metadata store
        self._add_metadata_store(path)

        # Build artifact stores
        try:
            for cfg in configs:
                self.add_artifact_store(cfg)
        except TypeError:
            pass

    def _add_metadata_store(self, path: str) -> None:
        """
        Add a metadata store to the registry.
        """
        if self._md_store is None:
            self._md_store = StoreBuilder().build_metadata_store(path)

    def add_artifact_store(self, config: dict) -> None:
        """
        Add an artifact store to the registry.

        Parameters
        ----------
        config : dict
            Store configuration dictionary.

        Returns
        -------
        None
        """
        store = StoreBuilder().build_artifact_store(self._tmp_dir, config)
        if store.is_default or self._default_store is None:
            self._default_store = store
        self._stores[store.name] = store

    def get_md_store(self) -> MetadataStore:
        """
        Get metadata store from registry.

        Returns
        -------
        MetadataStore
            Metadata store.
        """
        return self._md_store

    def get_art_store(self, name: str) -> ArtifactStore:
        """
        Get artifact store from registry by name.

        Parameters
        ----------
        name : str
            Name of the store.

        Returns
        -------
        ArtifactStore
            Artifact store.
        """
        return self._stores[name]

    def get_def_store(self) -> ArtifactStore:
        """
        Get default artifact store from registry.

        Returns
        -------
        ArtifactStore
            Artifact store.
        """
        return self._default_store

    def get_all_art_stores(self) -> list[ArtifactStore]:
        """
        Get all artifact stores from registry.

        Returns
        -------
        list[ArtifactStore]
            List of artifact stores.
        """
        return list(self._stores.values())

    def clean_all(self) -> None:
        """
        Clean up temporary download directory contents.

        Returns
        -------
        None
        """
        self._clean_temp_path_store_cache()
        try:
            clean_all(self._tmp_dir)
        except FileNotFoundError:
            pass

    def _clean_temp_path_store_cache(self) -> None:
        """
        Get rid of reference to temporary paths stored in artifact stores.

        Returns
        -------
        None
        """
        for store in self.get_all_art_stores():
            store.clean_paths()
