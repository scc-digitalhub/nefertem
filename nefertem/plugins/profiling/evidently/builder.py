"""
Evidently profile plugin builder module.
"""
from __future__ import annotations

import typing

from nefertem.plugins.profiling.base import ProfilingPluginBuilder
from nefertem.plugins.profiling.evidently.metrics import MetricEvidently
from nefertem.plugins.profiling.evidently.plugin import ProfilePluginEvidently
from nefertem.utils.commons import BASE_FILE_READER

if typing.TYPE_CHECKING:
    from nefertem.resources.data_resource import DataResource


class ProfileBuilderEvidently(ProfilingPluginBuilder):
    """
    Evidently profile plugin builder.
    """

    def build(self, resources: list[DataResource], metrics: list[dict]) -> list[ProfilePluginEvidently]:
        """
        Build a plugin for every metric element.
        """
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
    def _filter_metrics(metrics: list[dict]) -> list[MetricEvidently]:
        """
        Build metrics.
        """
        mets = []
        for met in metrics:
            if met.get("type") == "evidently":
                mets.append(MetricEvidently(**met))
        return mets

    def destroy(self) -> None:
        """
        Destory plugins.
        """
