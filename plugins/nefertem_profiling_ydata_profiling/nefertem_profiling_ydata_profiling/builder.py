from __future__ import annotations

import typing
from copy import deepcopy

from nefertem_profiling.plugins.builder import ProfilingPluginBuilder
from nefertem_profiling_ydata_profiling.plugin import ProfilingPluginYdataProfiling

from nefertem.readers.builder import build_reader
from nefertem.readers.registry import reader_registry

if typing.TYPE_CHECKING:
    from nefertem.resources.data_resource import DataResource


DF_READER = "pandas_df_reader"


class ProfilingBuilderYdataProfiling(ProfilingPluginBuilder):
    """
    Profile plugin builder.
    """

    def __init__(self, stores: dict[str, str], exec_args: dict) -> None:
        super().__init__(stores, exec_args)
        reader_registry.register(DF_READER, "nefertem_profiling_ydata_profiling.reader", "PandasDataFrameFileReader")

    def build(self, resources: list[DataResource]) -> list[ProfilingPluginYdataProfiling]:
        """
        Build a plugin.
        """
        plugins = []
        for res in resources:
            resource = deepcopy(res)
            store = self.stores[resource.store]
            data_reader = build_reader(DF_READER, store)
            plugin = ProfilingPluginYdataProfiling()
            plugin.setup(data_reader, resource, self.exec_args)
            plugins.append(plugin)
        return plugins
