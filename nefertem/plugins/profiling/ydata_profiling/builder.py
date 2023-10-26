from nefertem.plugins.profiling.base import Metric, ProfilingPluginBuilder
from nefertem.plugins.profiling.ydata_profiling.plugin import ProfilePluginYdataProfiling
from nefertem.resources.data_resource import DataResource
from nefertem.utils.commons import PANDAS_DATAFRAME_FILE_READER


class ProfileBuilderYdataProfiling(ProfilingPluginBuilder):
    """
    Profile plugin builder.
    """

    def build(
        self, resources: list[DataResource], metrics: list[Metric] | None = None
    ) -> list[ProfilePluginYdataProfiling]:
        """
        Build a plugin.
        """
        plugins = []
        for res in resources:
            resource = self._get_resource_deepcopy(res)
            store = self._get_resource_store(resource)
            data_reader = self._get_data_reader(PANDAS_DATAFRAME_FILE_READER, store)
            plugin = ProfilePluginYdataProfiling()
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
