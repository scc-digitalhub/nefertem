from __future__ import annotations

import typing
from abc import abstractmethod
from copy import deepcopy

from nefertem.readers.builder import build_reader
from nefertem.utils.exceptions import StoreError

if typing.TYPE_CHECKING:
    from nefertem.plugins.plugin import Plugin
    from nefertem.readers.base import DataReader
    from nefertem.resources.data_resource import DataResource
    from nefertem.stores.input.objects.base import InputStore


class PluginBuilder:
    """
    Abstract PluginBuilder class.
    """

    def __init__(self, stores: list[InputStore], exec_args: dict) -> None:
        self.stores = stores
        self.exec_args = exec_args

    @abstractmethod
    def build(self, *args, **kwargs) -> list[Plugin]:
        """
        Build a list of plugin.
        """

    @staticmethod
    def _get_resource_deepcopy(resource: DataResource) -> DataResource:
        """
        Return deepcopy of a resource.
        """
        return deepcopy(resource)

    def _get_resource_store(self, resource: DataResource) -> InputStore:
        """
        Get the resource store.
        """
        try:
            return [store for store in self.stores if store.name == resource.store][0]
        except IndexError:
            raise StoreError(
                f"No store registered with name '{resource.store}'. Impossible to fetch resource '{resource.name}'"
            )

    @staticmethod
    def _get_data_reader(type: str, store: InputStore) -> DataReader:
        """
        Get data reader.
        """
        return build_reader(type, store)
