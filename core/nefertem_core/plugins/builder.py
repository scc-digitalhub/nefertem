from __future__ import annotations

import typing
from abc import abstractmethod

if typing.TYPE_CHECKING:
    from nefertem_core.plugins.plugin import Plugin
    from nefertem_core.stores.input.objects._base import InputStore


class PluginBuilder:
    """
    Abstract PluginBuilder class.
    """

    def __init__(self, stores: list[InputStore], exec_args: dict) -> None:
        self.exec_args = exec_args
        self.stores = {store.name: store for store in stores}

    @abstractmethod
    def build(self, *args, **kwargs) -> list[Plugin]:
        """
        Build a list of plugin.
        """
