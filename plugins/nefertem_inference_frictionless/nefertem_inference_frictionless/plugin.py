"""
Frictionless inference plugin module.
"""
from __future__ import annotations

import typing

import frictionless
from frictionless import Schema
from nefertem_inference.metadata.report import NefertemSchema
from nefertem_inference.plugins.plugin import InferencePlugin
from nefertem_inference.plugins.utils import get_fields

from nefertem.plugins.utils import RenderTuple, exec_decorator

if typing.TYPE_CHECKING:
    from nefertem.plugins.utils import Result
    from nefertem.readers.objects.file import FileReader
    from nefertem.resources.data_resource import DataResource


class InferencePluginFrictionless(InferencePlugin):
    """
    Frictionless implementation of inference plugin.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        super().__init__()
        self.resource = None
        self.exec_multiprocess = True

    def setup(self, data_reader: FileReader, resource: DataResource, exec_args: dict) -> None:
        """
        Set plugin resource.

        Parameters
        ----------
        data_reader : FileReader
            Data reader.
        resource : DataResource
            Data resource to be inferred.
        exec_args : dict
            Execution arguments for Schema.describe.

        Returns
        -------
        None
        """
        self.data_reader = data_reader
        self.resource = resource
        self.exec_args = exec_args

    @exec_decorator
    def infer(self) -> Schema:
        """
        Method that call infer on a resource and return an inferred schema.

        Returns
        -------
        Schema
            Inferred schema.
        """
        data = self.data_reader.fetch_data(self.resource.path)
        schema = Schema.describe(path=str(data), name=self.resource.name, **self.exec_args)
        return Schema(schema.to_dict())

    @exec_decorator
    def render_nefertem(self, result: Result) -> NefertemSchema:
        """
        Method that call render on a resource and return a NefertemSchema.

        Parameters
        ----------
        result : Result
            Execution result.

        Returns
        -------
        NefertemSchema
            NefertemSchema.
        """
        exec_err = result.errors
        duration = result.duration

        if exec_err is None:
            inferred = result.artifact.to_dict().get("fields", [])
            fields = [get_fields(i.get("name", ""), i.get("type", "")) for i in inferred]
        else:
            self.logger.error(f"Execution error {str(exec_err)} for plugin {self.id}")
            fields = []
        return NefertemSchema(self.framework_name(), self.framework_version(), duration, fields)

    @exec_decorator
    def render_artifact(self, result: Result) -> list[tuple]:
        """
        Return a frictionless schema to be persisted as artifact.

        Parameters
        ----------
        result : Result
            Execution result.

        Returns
        -------
        list[tuple]
            List of RenderTuple.
        """
        if result.artifact is None:
            obj = {"errors": result.errors}
        else:
            obj = result.artifact.to_dict()
        filename = self._fn_schema.format("frictionless.json")
        return [RenderTuple(obj, filename)]

    @staticmethod
    def framework_name() -> str:
        """
        Get library name.

        Returns
        -------
        str
            Library name.
        """
        return frictionless.__name__

    @staticmethod
    def framework_version() -> str:
        """
        Get library version.

        Returns
        -------
        str
            Library version.
        """
        return frictionless.__version__
