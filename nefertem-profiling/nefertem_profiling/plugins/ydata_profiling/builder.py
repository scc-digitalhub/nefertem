from __future__ import annotations

import typing

from nefertem_profiling.plugins.builder import ProfilingPluginBuilder
from nefertem_profiling.plugins.ydata_profiling.plugin import ProfilingPluginYdataProfiling
from nefertem.utils.commons import PANDAS_DATAFRAME_FILE_READER

if typing.TYPE_CHECKING:
    from nefertem.resources.data_resource import DataResource


class ProfilingBuilderYdataProfiling(ProfilingPluginBuilder):
    """
    Profile plugin builder.
    """

    def build(self, resources: list[DataResource], *args) -> list[ProfilingPluginYdataProfiling]:
        """
        Build a plugin.
        """
        plugins = []
        for res in resources:
            resource = self._get_resource_deepcopy(res)
            store = self._get_resource_store(resource)
            data_reader = self._get_data_reader(PANDAS_DATAFRAME_FILE_READER, store)
            plugin = ProfilingPluginYdataProfiling()
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
