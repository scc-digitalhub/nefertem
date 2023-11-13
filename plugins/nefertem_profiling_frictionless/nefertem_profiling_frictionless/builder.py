from __future__ import annotations

import typing
from copy import deepcopy

from nefertem_profiling.plugins.builder import ProfilingPluginBuilder
from nefertem_profiling_frictionless.plugin import ProfilingPluginFrictionless

from nefertem.readers.builder import build_reader
from nefertem.utils.commons import FILE_READER

if typing.TYPE_CHECKING:
    from nefertem.resources.data_resource import DataResource


class ProfilingBuilderFrictionless(ProfilingPluginBuilder):
    """
    Profile plugin builder.
    """

    def build(self, resources: list[DataResource]) -> list[ProfilingPluginFrictionless]:
        """
        Build a plugin. Metrics are not supported
        """
        plugins = []
        for res in resources:
            resource = deepcopy(res)
            store = self.stores[resource.store]
            data_reader = build_reader(FILE_READER, store)
            plugin = ProfilingPluginFrictionless()
            plugin.setup(data_reader, resource, self.exec_args)
            plugins.append(plugin)
        return plugins
