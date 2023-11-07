"""
InputStore registry.
"""
from __future__ import annotations

import typing

from nefertem.stores.input.objects.dummy import DummyInputStore, DummyStoreConfig
from nefertem.stores.input.objects.local import LocalInputStore, LocalStoreConfig
from nefertem.stores.input.objects.remote import RemoteInputStore, RemoteStoreConfig
from nefertem.stores.input.objects.s3 import S3InputStore, S3StoreConfig
from nefertem.stores.input.objects.sql import SQLInputStore, SQLStoreConfig
from nefertem.stores.kinds import StoreKinds

if typing.TYPE_CHECKING:
    from nefertem.stores.input.objects._base import InputStore, StoreConfig


class InputStoreRegistry(dict):
    """
    Generic registry for InputStore objects.
    """

    def register(self, kind: str, store: InputStore, model: StoreConfig) -> None:
        """
        Register a new store.

        Parameters
        ----------
        kind : str
            The store kind.
        store : InputStore
            The store object.
        """
        self[kind] = {}
        self[kind]["store"] = store
        self[kind]["model"] = model


input_store_registry = InputStoreRegistry()
input_store_registry.register(StoreKinds.DUMMY.value, DummyInputStore, DummyStoreConfig)
input_store_registry.register(StoreKinds.LOCAL.value, LocalInputStore, LocalStoreConfig)
input_store_registry.register(StoreKinds.S3.value, S3InputStore, S3StoreConfig)
input_store_registry.register(StoreKinds.REMOTE.value, RemoteInputStore, RemoteStoreConfig)
input_store_registry.register(StoreKinds.SQL.value, SQLInputStore, SQLStoreConfig)
