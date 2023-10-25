"""
Frictionless implementation of profiling plugin.
"""
from __future__ import annotations

import typing

import frictionless
from frictionless import Resource

from nefertem.metadata.reports.profile import NefertemProfile
from nefertem.plugins.profiling.base import Profiling, ProfilingPluginBuilder
from nefertem.plugins.utils.plugin_utils import exec_decorator
from nefertem.utils.commons import BASE_FILE_READER
from nefertem.utils.io_utils import write_bytesio

if typing.TYPE_CHECKING:
    from nefertem.plugins.profiling.base import Metric
    from nefertem.plugins.utils.plugin_utils import Result
    from nefertem.readers.base.file import FileReader
    from nefertem.resources.data_resource import DataResource


####################
# PLUGIN
####################


class ProfilePluginFrictionless(Profiling):
    """
    Frictionless implementation of profiling plugin.
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
    def profile(self) -> Resource:
        """
        Profile
        """
        data = self.data_reader.fetch_data(self.resource.path)
        profile = Resource().describe(data, stats=True, **self.exec_args)
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
            self.logger.error(f"Execution error {str(exec_err)} for plugin {self._id}")
            fields = {}
            stats = {}

        return NefertemProfile(self.get_lib_name(), self.get_lib_version(), duration, stats, fields)

    @exec_decorator
    def render_artifact(self, result: Result) -> list[tuple]:
        """
        Return a rendered profile ready to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
        else:
            _object = write_bytesio(result.artifact.to_json())
        filename = self._fn_profile.format("frictionless.json")
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


####################
# BUILDER
####################


class ProfileBuilderFrictionless(ProfilingPluginBuilder):
    """
    Profile plugin builder.
    """

    def build(
        self, resources: list[DataResource], metrics: list[Metric] | None = None
    ) -> list[ProfilePluginFrictionless]:
        """
        Build a plugin. Metrics are not supported
        """
        plugins = []
        for res in resources:
            resource = self._get_resource_deepcopy(res)
            store = self._get_resource_store(resource)
            data_reader = self._get_data_reader(BASE_FILE_READER, store)
            plugin = ProfilePluginFrictionless()
            plugin.setup(data_reader, resource, self.exec_args)
            plugins.append(plugin)
        return plugins

    @staticmethod
    def _filter_metrics(*args) -> None:
        """
        Placeholder methods.

        Returns
        -------
        None
        """