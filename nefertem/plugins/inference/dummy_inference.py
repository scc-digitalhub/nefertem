"""
Dummy implementation of inference plugin.
"""
from __future__ import annotations

import typing

from nefertem.metadata.reports.schema import NefertemSchema
from nefertem.plugins.inference.inference_plugin import Inference, InferencePluginBuilder
from nefertem.plugins.utils.plugin_utils import exec_decorator
from nefertem.utils.commons import DUMMY, LIBRARY_DUMMY

if typing.TYPE_CHECKING:
    from nefertem.plugins.utils.plugin_utils import Result


class InferencePluginDummy(Inference):
    """
    Dummy implementation of inference plugin.
    """

    def setup(self, *args) -> None:
        ...

    @exec_decorator
    def infer(self) -> dict:
        """
        Do nothing.
        """
        return {}

    @exec_decorator
    def render_nefertem(self, *args) -> NefertemSchema:
        """
        Return a NefertemSchema.
        """
        return NefertemSchema(self.get_lib_name(), self.get_lib_version(), 0.0, [])

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
        filename = self._fn_schema.format(f"{DUMMY}.json")
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


class InferenceBuilderDummy(InferencePluginBuilder):
    """
    Inference plugin builder.
    """

    def build(self, *args) -> list[InferencePluginDummy]:
        """
        Build a plugin.
        """
        return [InferencePluginDummy()]
