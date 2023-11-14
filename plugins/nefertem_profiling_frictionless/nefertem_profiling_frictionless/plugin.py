"""
Frictionless implementation of profiling plugin.
"""
from __future__ import annotations

import typing

import frictionless
from frictionless import Resource
from nefertem_profiling.metadata.report import NefertemProfile
from nefertem_profiling.plugins.plugin import ProfilingPlugin

from nefertem.plugins.utils import RenderTuple, exec_decorator
from nefertem.utils.io_utils import write_bytesio

if typing.TYPE_CHECKING:
    from nefertem.plugins.utils import Result
    from nefertem.readers.objects.file import FileReader
    from nefertem.resources.data_resource import DataResource


class ProfilingPluginFrictionless(ProfilingPlugin):
    """
    Frictionless implementation of profiling plugin.
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
        """
        self.data_reader = data_reader
        self.resource = resource
        self.exec_args = exec_args

    @exec_decorator
    def profile(self) -> Resource:
        """
        Profile
        """
        data = self.data_reader.fetch_data(self.resource.path)
        profile = Resource().describe(str(data), stats=True, **self.exec_args)
        return Resource(profile.to_dict())

    @exec_decorator
    def render_nefertem(self, result: Result) -> NefertemProfile:
        """
        Return a NefertemProfile.
        """
        exec_err = result.errors
        duration = result.duration

        if exec_err is None:
            rep = result.artifact.to_dict()
            fields = rep.get("schema", {}).get("fields")
            fields = {f["name"]: {"type": f["type"]} for f in fields}
            stats = {k: v for k, v in rep.items() if k != "schema"}
        else:
            self.logger.error(f"Execution error {str(exec_err)} for plugin {self.id}")
            fields = {}
            stats = {}

        return NefertemProfile(self.framework_name(), self.framework_version(), duration, stats, fields)

    @exec_decorator
    def render_artifact(self, result: Result) -> list[tuple]:
        """
        Return a rendered profile ready to be persisted as artifact.
        """
        if result.artifact is None:
            obj = {"errors": result.errors}
        else:
            obj = write_bytesio(result.artifact.to_json())
        filename = self._fn_profile.format("frictionless.json")
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
