from nefertem.plugins.profiling.base import Metric, ProfilingPluginBuilder
from nefertem.plugins.profiling.frictionless.plugin import ProfilePluginFrictionless
from nefertem.resources.data_resource import DataResource
from nefertem.utils.commons import BASE_FILE_READER


class ProfileBuilderFrictionless(ProfilingPluginBuilder):
    """
    Profile plugin builder.
    """

    def build(
        self, resources: list[DataResource], metrics: list[Metric] | None = None
    ) -> list[ProfilePluginFrictionless]:
        """
        Build a plugin. Metrics are not supported
        """
        plugins = []
        for res in resources:
            resource = self._get_resource_deepcopy(res)
            store = self._get_resource_store(resource)
            data_reader = self._get_data_reader(BASE_FILE_READER, store)
            plugin = ProfilePluginFrictionless()
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
