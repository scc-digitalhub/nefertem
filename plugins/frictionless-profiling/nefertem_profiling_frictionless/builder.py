from __future__ import annotations

import typing
from copy import deepcopy

from nefertem_core.readers.builder import build_reader
from nefertem_core.utils.commons import FILE_READER
from nefertem_profiling.plugins.builder import ProfilingPluginBuilder
from nefertem_profiling_frictionless.plugin import ProfilingPluginFrictionless

if typing.TYPE_CHECKING:
    from nefertem_core.resources.data_resource import DataResource


class ProfilingBuilderFrictionless(ProfilingPluginBuilder):
    """
    Profile plugin builder.
    """

    def build(self, resources: list[DataResource]) -> list[ProfilingPluginFrictionless]:
        """
        Build a plugin for each resource.

        Parameters
        ----------
        resources : list[DataResource]
            List of resources.

        Returns
        -------
        list[ProfilingPluginFrictionless]
            List of plugins.
        """
        plugins = []
        for res in resources:
            # Get data reader for the resource
            data_reader = build_reader(FILE_READER, self.stores[res.store])

            # Build and setup plugin with a copy of the resource to avoid
            # resource modification
            plugin = ProfilingPluginFrictionless()
            plugin.setup(data_reader, deepcopy(res), self.exec_args)
            plugins.append(plugin)
        return plugins
