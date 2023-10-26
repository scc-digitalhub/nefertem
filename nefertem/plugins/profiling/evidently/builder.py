"""
Evidently profile plugin builder module.
"""
import evidently

from nefertem.plugins.profiling.base import Metric, ProfilingPluginBuilder
from nefertem.plugins.profiling.evidently.plugin import ProfilePluginEvidently
from nefertem.resources.data_resource import DataResource
from nefertem.utils.commons import BASE_FILE_READER


class ProfileBuilderEvidently(ProfilingPluginBuilder):
    """
    Evidently profile plugin builder.
    """

    def build(self, resources: list[DataResource], metrics: list[Metric] | None = None) -> list[ProfilePluginEvidently]:
        """
        Build a plugin for every metric element.
        """
        if metrics is None or len(metrics) == 0:
            return []

        f_metrics = self._filter_metrics(metrics)
        plugins = []
        for metric in f_metrics:
            data_reader = None
            curr_resource = None
            ref_data_reader = None
            ref_resource = None
            for resource in resources:
                if resource.name == metric.resource:
                    store = self._get_resource_store(resource)
                    data_reader = self._get_data_reader(BASE_FILE_READER, store)
                    curr_resource = resource
                elif resource.name == metric.reference_resource:
                    store = self._get_resource_store(resource)
                    ref_data_reader = self._get_data_reader(BASE_FILE_READER, store)
                    ref_resource = resource

            if curr_resource is not None:
                plugin = ProfilePluginEvidently()
                plugin.setup(data_reader, resource, metric, self.exec_args, ref_data_reader, ref_resource)
                plugins.append(plugin)

        return plugins

    @staticmethod
    def _filter_metrics(metrics: list[Metric]) -> list[Metric]:
        """
        Filter out MetricEvidently.
        """
        if metrics is None:
            return []
        return [m for m in metrics if m.type == evidently]

    def destroy(self) -> None:
        """
        Destory plugins.
        """
