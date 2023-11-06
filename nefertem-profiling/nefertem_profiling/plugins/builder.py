"""
Profiling plugin abstract class module.
"""
from abc import abstractmethod

from nefertem.plugins.builder import PluginBuilder
from nefertem_profiling.plugins.metric import Metric


class ProfilingPluginBuilder(PluginBuilder):
    """
    Profiling plugin builder.
    """

    @staticmethod
    @abstractmethod
    def _filter_metrics(metrics: list[Metric]) -> list[Metric]:
        """
        Filter metric by library.
        """
