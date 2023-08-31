"""
Profiling plugin abstract class module.
"""
from abc import ABCMeta, abstractmethod
from typing import Any, List

from nefertem.plugins.base_plugin import Plugin, PluginBuilder
from nefertem.utils.commons import (
    RESULT_WRAPPED,
    RESULT_NEFERTEM,
    RESULT_RENDERED,
    RESULT_LIBRARY,
)


class Profiling(Plugin, metaclass=ABCMeta):
    """
    Run plugin that executes profiling over a Resource.
    """

    _fn_profile = "profile_{}"

    def __init__(self) -> None:
        super().__init__()
        self.metric = None

    def execute(self) -> dict:
        """
        Method that call specific execution.
        """
        plugin = f"Plugin: {self.lib_name} {self._id};"
        self.logger.info(f"Execute profiling - {plugin}" + (' Metric: {self.metric.name}' if self.metric is not None else ''))
        lib_result = self.profile()
        self.logger.info(f"Render report - {plugin}")
        nt_result = self.render_nefertem(lib_result)
        self.logger.info(f"Render artifact - {plugin}")
        render_result = self.render_artifact(lib_result)
        return {
            RESULT_WRAPPED: lib_result,
            RESULT_NEFERTEM: nt_result,
            RESULT_RENDERED: render_result,
            RESULT_LIBRARY: self.get_library(),
        }

    @abstractmethod
    def profile(self) -> Any:
        """
        Generate a data profile.
        """

class ProfilingPluginBuilder(PluginBuilder):
    """
    Validation plugin builder.
    """

    @staticmethod
    @abstractmethod
    def _filter_metrics(metrics: List["Metric"]) -> List["Metric"]:
        """
        Filter metric by library.
        """
