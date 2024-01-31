"""
Profiling plugin abstract class module.
"""
from __future__ import annotations

from abc import abstractmethod

from nefertem_core.plugins.builder import PluginBuilder
from nefertem_metric.plugins.metric import Metric


class MetricPluginBuilder(PluginBuilder):
    """
    Profiling plugin builder.
    """

    @staticmethod
    @abstractmethod
    def _filter_metrics(metrics: list[Metric]) -> list[Metric]:
        """
        Filter metric by library.
        """
