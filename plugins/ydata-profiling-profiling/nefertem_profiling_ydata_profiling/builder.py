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
        """
        Constructor.
        """
        super().__init__(stores, exec_args)

        # Register new reader in the reader registry
        reader_registry.register(
            DF_READER,
            "nefertem_profiling_ydata_profiling.reader",
            "PandasDataFrameFileReader",
        )

    def build(self, resources: list[DataResource]) -> list[ProfilingPluginYdataProfiling]:
        """
        Build a plugin for each resource.

        Parameters
        ----------
        resources : list[DataResource]
            List of resources.

        Returns
        -------
        list[ProfilingPluginYdataProfiling]
            List of plugins.
        """
        plugins = []
        for res in resources:
            # Get data reader for the resource
            data_reader = build_reader(DF_READER, self.stores[res.store])

            # Build and setup plugin with a copy of the resource to avoid
            # resource modification
            plugin = ProfilingPluginYdataProfiling()
            plugin.setup(data_reader, deepcopy(res), self.exec_args)
            plugins.append(plugin)
        return plugins
