"""
ArtifactStore registry.
"""
from __future__ import annotations

import typing

from nefertem.stores.artifact.objects.dummy import DummyArtifactStore, DummyStoreConfig
from nefertem.stores.artifact.objects.local import LocalArtifactStore, LocalStoreConfig
from nefertem.stores.artifact.objects.remote import RemoteArtifactStore, RemoteStoreConfig
from nefertem.stores.artifact.objects.s3 import S3ArtifactStore, S3StoreConfig
from nefertem.stores.artifact.objects.sql import SQLArtifactStore, SQLStoreConfig
from nefertem.stores.kinds import StoreKinds

if typing.TYPE_CHECKING:
    from nefertem.stores.artifact.objects.base import ArtifactStore, StoreConfig


class ArtifactStoreRegistry(dict):
    """
    Generic registry for ArtifactStore objects.
    """

    def register(self, kind: str, store: ArtifactStore, model: StoreConfig) -> None:
        """
        Register a new store.

        Parameters
        ----------
        kind : str
            The store kind.
        store : ArtifactStore
            The store object.
        """
        self[kind] = {}
        self[kind]["store"] = store
        self[kind]["model"] = model


artstore_registry = ArtifactStoreRegistry()
artstore_registry.register(StoreKinds.DUMMY.value, DummyArtifactStore, DummyStoreConfig)
artstore_registry.register(StoreKinds.LOCAL.value, LocalArtifactStore, LocalStoreConfig)
artstore_registry.register(StoreKinds.S3.value, S3ArtifactStore, S3StoreConfig)
artstore_registry.register(StoreKinds.REMOTE.value, RemoteArtifactStore, RemoteStoreConfig)
artstore_registry.register(StoreKinds.SQL.value, SQLArtifactStore, SQLStoreConfig)
