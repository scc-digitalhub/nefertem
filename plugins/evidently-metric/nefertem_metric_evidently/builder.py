"""
Evidently profile plugin builder module.
"""
from __future__ import annotations

import typing

from nefertem_core.readers.builder import build_reader
from nefertem_core.utils.commons import FILE_READER
from nefertem_metric_evidently.metrics import MetricEvidently
from nefertem_metric_evidently.plugin import ProfilingPluginEvidently
from nefertem_profiling.plugins.builder import ProfilingPluginBuilder

if typing.TYPE_CHECKING:
    from nefertem_core.resources.data_resource import DataResource


class MetricBuilderEvidently(ProfilingPluginBuilder):
    """
    Evidently profile plugin builder.
    """

    def build(self, resources: list[DataResource], metrics: list[dict]) -> list[ProfilingPluginEvidently]:
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
                    store = self.stores[resource.store]
                    data_reader = build_reader(FILE_READER, store)
                    curr_resource = resource
                elif resource.name == metric.reference_resource:
                    store = self.stores[resource.store]
                    ref_data_reader = build_reader(FILE_READER, store)
                    ref_resource = resource

            if curr_resource is not None:
                plugin = ProfilingPluginEvidently()
                plugin.setup(
                    data_reader,
                    resource,
                    metric,
                    self.exec_args,
                    ref_data_reader,
                    ref_resource,
                )
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
