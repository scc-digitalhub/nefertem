"""
Dummy implementation of profiling plugin.
"""

from __future__ import annotations

import typing

from nefertem_profiling.metadata.report import NefertemProfile
from nefertem_profiling.plugins.plugin import ProfilingPlugin

from nefertem.plugins.utils import exec_decorator
from nefertem.utils.commons import DUMMY

if typing.TYPE_CHECKING:
    from nefertem.plugins.utils import Result


class ProfilingPluginDummy(ProfilingPlugin):
    """
    Dummy implementation of profiling plugin.
    """

    def __init__(self) -> None:
        super().__init__()

    def setup(self, *args) -> None:
        """
        Placeholder methods.

        Returns
        -------
        None
        """

    @exec_decorator
    def profile(self) -> dict:
        """
        Do nothing.
        """
        return {}

    @exec_decorator
    def render_nefertem(self, *args) -> NefertemProfile:
        """
        Return a NefertemProfile.
        """
        return NefertemProfile(self.get_lib_name(), self.get_lib_version(), 0.0, {}, {})

    @exec_decorator
    def render_artifact(self, result: Result) -> list[tuple]:
        """
        Return a dummy schema to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
        else:
            _object = dict(result.artifact)
        filename = self._fn_profile.format(f"{DUMMY}.json")
        artifacts.append(self.get_render_tuple(_object, filename))
        return artifacts

    @staticmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """
        return DUMMY

    @staticmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """
        return DUMMY
