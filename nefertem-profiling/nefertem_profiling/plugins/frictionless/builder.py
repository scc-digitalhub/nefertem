from __future__ import annotations

import typing

from nefertem_profiling.plugins.builder import ProfilingPluginBuilder
from nefertem_profiling.plugins.frictionless.plugin import ProfilingPluginFrictionless
from nefertem.utils.commons import BASE_FILE_READER

if typing.TYPE_CHECKING:
    from nefertem.resources.data_resource import DataResource


class ProfilingBuilderFrictionless(ProfilingPluginBuilder):
    """
    Profile plugin builder.
    """

    def build(self, resources: list[DataResource], *args) -> list[ProfilingPluginFrictionless]:
        """
        Build a plugin. Metrics are not supported
        """
        plugins = []
        for res in resources:
            resource = self._get_resource_deepcopy(res)
            store = self._get_resource_store(resource)
            data_reader = self._get_data_reader(BASE_FILE_READER, store)
            plugin = ProfilingPluginFrictionless()
            plugin.setup(data_reader, resource, self.exec_args)
            plugins.append(plugin)
        return plugins

    @staticmethod
    def _filter_metrics(*args) -> None:
        """
        Placeholder methods.

        Returns
        -------
        None
        """
