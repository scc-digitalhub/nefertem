"""
Frictionless inference plugin module.
"""
from __future__ import annotations

import typing

import frictionless
from frictionless import Schema
from nefertem_inference.metadata.report import NefertemSchema
from nefertem_inference.plugins.plugin import InferencePlugin

from nefertem.plugins.utils import exec_decorator

if typing.TYPE_CHECKING:
    from nefertem.plugins.utils import Result
    from nefertem.readers.file.file import FileReader
    from nefertem.resources.data_resource import DataResource


class InferencePluginFrictionless(InferencePlugin):
    """
    Frictionless implementation of inference plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.resource = None
        self.exec_multiprocess = True

    def setup(self, data_reader: FileReader, resource: DataResource, exec_args: dict) -> None:
        """
        Set plugin resource.
        """
        self.data_reader = data_reader
        self.resource = resource
        self.exec_args = exec_args

    @exec_decorator
    def infer(self) -> Schema:
        """
        Method that call infer on a resource and return an inferred schema.
        """
        data = self.data_reader.fetch_data(self.resource.path)
        schema = Schema.describe(path=data, name=self.resource.name, **self.exec_args)
        return Schema(schema.to_dict())

    @exec_decorator
    def render_nefertem(self, result: Result) -> NefertemSchema:
        """
        Return a NefertemSchema.
        """

        exec_err = result.errors
        duration = result.duration

        if exec_err is None:
            inferred_fields = result.artifact.to_dict().get("fields", [])

            def func(x):
                return self._get_fields(x.get("name", ""), x.get("type", ""))

            fields = [func(field) for field in inferred_fields]
        else:
            self.logger.error(f"Execution error {str(exec_err)} for plugin {self._id}")
            fields = []

        return NefertemSchema(self.framework_name(), self.framework_version(), duration, fields)

    @exec_decorator
    def render_artifact(self, result: Result) -> list[tuple]:
        """
        Return a frictionless schema to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
        else:
            _object = result.artifact.to_dict()
        filename = self._fn_schema.format("frictionless.json")
        artifacts.append(self._get_render_tuple(_object, filename))
        return artifacts

    @staticmethod
    def framework_name() -> str:
        """
        Get library name.
        """
        return frictionless.__name__

    @staticmethod
    def framework_version() -> str:
        """
        Get library version.
        """
        return frictionless.__version__
