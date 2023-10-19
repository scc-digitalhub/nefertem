"""
MetadataStore registry.
"""
from __future__ import annotations

import typing

from nefertem.stores.kinds import StoreKinds
from nefertem.stores.metadata.objects.dummy import DummyMetadataStore
from nefertem.stores.metadata.objects.local import LocalMetadataStore

if typing.TYPE_CHECKING:
    from nefertem.stores.metadata.objects.base import MetadataStore


class MetadataStoreRegistry(dict):
    """
    Generic registry for MetadataStore objects.
    """

    def register(self, kind: str, store: MetadataStore) -> None:
        """
        Register a new store.

        Parameters
        ----------
        kind : str
            The store kind.
        store : MetadataStore
            The store object.
        """
        self[kind] = store


mdstore_registry = MetadataStoreRegistry()
mdstore_registry.register(StoreKinds.DUMMY.value, DummyMetadataStore)
mdstore_registry.register(StoreKinds.LOCAL.value, LocalMetadataStore)
