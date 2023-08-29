"""
Dummy implementation of inference plugin.
"""
# pylint: disable=unused-argument
from typing import List

from nefertem.metadata.nefertem_reports import NefertemSchema
from nefertem.plugins.base_plugin import PluginBuilder
from nefertem.plugins.inference.inference_plugin import Inference
from nefertem.plugins.utils.plugin_utils import exec_decorator
from nefertem.utils.commons import GENERIC_DUMMY, LIBRARY_DUMMY


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
    def render_artifact(self, result: "Result") -> List[tuple]:
        """
        Return a dummy schema to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
        else:
            _object = dict(result.artifact)
        filename = self._fn_schema.format(f"{GENERIC_DUMMY}.json")
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


class InferenceBuilderDummy(PluginBuilder):
    """
    Inference plugin builder.
    """

    def build(self, *args) -> List[InferencePluginDummy]:
        """
        Build a plugin.
        """
        return [InferencePluginDummy()]

    def destroy(self) -> None:
        ...
