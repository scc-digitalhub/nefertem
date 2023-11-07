"""
Profiling plugin abstract class module.
"""
from abc import abstractmethod

from nefertem_profiling.plugins.metric import Metric

from nefertem.plugins.builder import PluginBuilder


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
