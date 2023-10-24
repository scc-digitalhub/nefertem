"""
Frictionless implementation of inference plugin.
"""
from __future__ import annotations

import typing

import frictionless
from frictionless.schema import Schema

from nefertem.metadata.reports.schema import NefertemSchema
from nefertem.plugins.inference.inference_plugin import Inference, InferencePluginBuilder
from nefertem.plugins.utils.plugin_utils import exec_decorator
from nefertem.utils.commons import BASE_FILE_READER, LIBRARY_FRICTIONLESS

if typing.TYPE_CHECKING:
    from nefertem.plugins.utils.plugin_utils import Result
    from nefertem.readers.base.file import FileReader
    from nefertem.resources.data_resource import DataResource


class InferencePluginFrictionless(Inference):
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
        Method that call infer on a resource and return an
        inferred schema.
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
            inferred_fields = result.artifact.get("fields", [])

            def func(x):
                return self._get_fields(x.get("name", ""), x.get("type", ""))

            fields = [func(field) for field in inferred_fields]
        else:
            self.logger.error(f"Execution error {str(exec_err)} for plugin {self._id}")
            fields = []

        return NefertemSchema(self.get_lib_name(), self.get_lib_version(), duration, fields)

    @exec_decorator
    def render_artifact(self, result: Result) -> list[tuple]:
        """
        Return a frictionless schema to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
        else:
            _object = dict(result.artifact)
        filename = self._fn_schema.format(f"{LIBRARY_FRICTIONLESS}.json")
        artifacts.append(self.get_render_tuple(_object, filename))
        return artifacts

    @staticmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """
        return frictionless.__name__

    @staticmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """
        return frictionless.__version__


class InferenceBuilderFrictionless(InferencePluginBuilder):
    """
    Inference plugin builder.
    """

    def build(self, resources: list[DataResource]) -> list[InferencePluginFrictionless]:
        """
        Build a plugin.
        """
        plugins = []
        for res in resources:
            resource = self._get_resource_deepcopy(res)
            store = self._get_resource_store(resource)
            data_reader = self._get_data_reader(BASE_FILE_READER, store)
            plugin = InferencePluginFrictionless()
            plugin.setup(data_reader, resource, self.exec_args)
            plugins.append(plugin)
        return plugins
