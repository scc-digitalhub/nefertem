"""
Dummy implementation of profiling plugin.
"""
# pylint: disable=unused-argument
from typing import List

from nefertem.metadata.reports.profile import NefertemProfile
from nefertem.plugins.profiling.profiling_plugin import Profiling, ProfilingPluginBuilder
from nefertem.plugins.utils.plugin_utils import exec_decorator
from nefertem.utils.commons import GENERIC_DUMMY, LIBRARY_DUMMY


class ProfilePluginDummy(Profiling):
    """
    Dummy implementation of profiling plugin.
    """

    def __init__(self) -> None:
        super().__init__()

    def setup(self, *args) -> None:
        ...

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
    def render_artifact(self, result: "Result") -> List[tuple]:
        """
        Return a dummy schema to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
        else:
            _object = dict(result.artifact)
        filename = self._fn_profile.format(f"{GENERIC_DUMMY}.json")
        artifacts.append(self.get_render_tuple(_object, filename))
        return artifacts

    @staticmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """
        return LIBRARY_DUMMY

    @staticmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """
        return LIBRARY_DUMMY


class ProfileBuilderDummy(ProfilingPluginBuilder):
    """
    Profile plugin builder.
    """

    def build(self, resources: List["DataResource"]) -> List[ProfilePluginDummy]:
        """
        Build a plugin.
        """
        return [ProfilePluginDummy()]

    @staticmethod
    def _filter_metrics(*args) -> None:
        ...

    def destroy(self) -> None:
        ...
