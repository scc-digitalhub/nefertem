"""
ArtifactStore registry.
"""
from __future__ import annotations

import typing

from nefertem.stores.artifact.objects.azure import AzureArtifactStore
from nefertem.stores.artifact.objects.dummy import DummyArtifactStore
from nefertem.stores.artifact.objects.ftp import FTPArtifactStore
from nefertem.stores.artifact.objects.http import HTTPArtifactStore
from nefertem.stores.artifact.objects.local import LocalArtifactStore
from nefertem.stores.artifact.objects.odbc import ODBCArtifactStore
from nefertem.stores.artifact.objects.s3 import S3ArtifactStore
from nefertem.stores.artifact.objects.sql import SQLArtifactStore
from nefertem.stores.kinds import StoreKinds

if typing.TYPE_CHECKING:
    from nefertem.stores.artifact.objects.base import ArtifactStore


class ArtifactStoreRegistry(dict):
    """
    Generic registry for ArtifactStore objects.
    """

    def register(self, kind: str, store: ArtifactStore) -> None:
        """
        Register a new store.

        Parameters
        ----------
        kind : str
            The store kind.
        store : ArtifactStore
            The store object.
        """
        self[kind] = store


artstore_registry = ArtifactStoreRegistry()
artstore_registry.register(StoreKinds.DUMMY.value, DummyArtifactStore)
artstore_registry.register(StoreKinds.LOCAL.value, LocalArtifactStore)
artstore_registry.register(StoreKinds.S3.value, S3ArtifactStore)
artstore_registry.register(StoreKinds.AZURE.value, AzureArtifactStore)
artstore_registry.register(StoreKinds.FTP.value, FTPArtifactStore)
artstore_registry.register(StoreKinds.HTTP.value, HTTPArtifactStore)
artstore_registry.register(StoreKinds.SQL.value, SQLArtifactStore)
artstore_registry.register(StoreKinds.ODBC.value, ODBCArtifactStore)
