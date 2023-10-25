"""
Profiling plugin abstract class module.
"""
from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any

from pydantic import BaseModel, Field

from nefertem.plugins.base import Plugin, PluginBuilder
from nefertem.utils.commons import RESULT_LIBRARY, RESULT_NEFERTEM, RESULT_RENDERED, RESULT_WRAPPED
from nefertem.utils.utils import build_uuid

####################
# PLUGIN
####################


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
        self.logger.info(
            f"Execute profiling - {plugin}" + (" Metric: {self.metric.name}" if self.metric is not None else "")
        )
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


####################
# BUILDER
####################


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

    def destroy(self, *args) -> None:
        """
        Placeholder methods.

        Returns
        -------
        None
        """


####################
# METRIC
####################


class Metric(BaseModel):
    """
    Base model for metric to be evaluated via profiling.
    """

    id: str = Field(default_factory=build_uuid)
    """UUID of metric."""

    name: str
    """Metric identificator as defined by the corresponding domain."""

    title: str
    """Human readable name for the metric."""

    resources: list[str]
    """List of resources on which the metric should be evaluated."""
