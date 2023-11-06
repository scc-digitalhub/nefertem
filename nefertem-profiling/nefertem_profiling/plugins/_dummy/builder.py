"""
Dummy implementation of profiling plugin.
"""

from __future__ import annotations

import typing

from nefertem_profiling.metadata.report import NefertemProfile
from nefertem_profiling.plugins.plugin import ProfilingPlugin
from nefertem_profiling.plugins.builder import ProfilingPluginBuilder
from nefertem.plugins.utils import exec_decorator
from nefertem.utils.commons import DUMMY

if typing.TYPE_CHECKING:
    from nefertem.plugins.utils import Result
    from nefertem.resources.data_resource import DataResource


class ProfilingBuilderDummy(ProfilingPluginBuilder):
    """
    Profile plugin builder.
    """

    def build(self, resources: list[DataResource]) -> list[ProfilingPluginDummy]:
        """
        Build a plugin.
        """
        return [ProfilingPluginDummy()]

    @staticmethod
    def _filter_metrics(*args) -> None:
        """
        Placeholder methods.

        Returns
        -------
        None
        """
