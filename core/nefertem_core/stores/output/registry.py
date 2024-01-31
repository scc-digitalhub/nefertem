"""
OutputStore registry.
"""
from __future__ import annotations

import typing

from nefertem_core.stores.kinds import StoreKinds
from nefertem_core.stores.output.objects.dummy import DummyOutputStore
from nefertem_core.stores.output.objects.local import LocalOutputStore

if typing.TYPE_CHECKING:
    from nefertem_core.stores.output.objects._base import OutputStore


class OutputStoreRegistry(dict):
    """
    Generic registry for OutputStore objects.
    """

    def register(self, kind: str, store: OutputStore) -> None:
        """
        Register a new store.

        Parameters
        ----------
        kind : str
            The store kind.
        store : OutputStore
            The store object.
        """
        self[kind] = store


mdstore_registry = OutputStoreRegistry()
mdstore_registry.register(StoreKinds.DUMMY.value, DummyOutputStore)
mdstore_registry.register(StoreKinds.LOCAL.value, LocalOutputStore)
