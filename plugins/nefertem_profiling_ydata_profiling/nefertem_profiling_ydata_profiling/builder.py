from __future__ import annotations

import typing
from copy import deepcopy

from nefertem_profiling.plugins.builder import ProfilingPluginBuilder
from nefertem_profiling_ydata_profiling.plugin import ProfilingPluginYdataProfiling

from nefertem.readers.builder import build_reader
from nefertem.utils.commons import PANDAS_DATAFRAME_FILE_READER

if typing.TYPE_CHECKING:
    from nefertem.resources.data_resource import DataResource


class ProfilingBuilderYdataProfiling(ProfilingPluginBuilder):
    """
    Profile plugin builder.
    """

    def build(self, resources: list[DataResource]) -> list[ProfilingPluginYdataProfiling]:
        """
        Build a plugin.
        """
        plugins = []
        for res in resources:
            resource = deepcopy(res)
            store = self.stores[resource.store]
            data_reader = build_reader(PANDAS_DATAFRAME_FILE_READER, store)
            plugin = ProfilingPluginYdataProfiling()
            plugin.setup(data_reader, resource, self.exec_args)
            plugins.append(plugin)
        return plugins
