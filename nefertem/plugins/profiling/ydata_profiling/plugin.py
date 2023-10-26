"""
Pandas profiling implementation of profiling plugin.
"""
from __future__ import annotations

import json
import typing

import ydata_profiling
from ydata_profiling import ProfileReport

from nefertem.metadata.nefertem import NefertemProfile
from nefertem.plugins.profiling.base import Profiling
from nefertem.plugins.profiling.ydata_profiling.utils import PROFILE_COLUMNS, PROFILE_FIELDS
from nefertem.plugins.utils import exec_decorator
from nefertem.utils.io_utils import write_bytesio

if typing.TYPE_CHECKING:
    from nefertem.plugins.utils import Result
    from nefertem.readers.file.native import NativeReader
    from nefertem.resources.data_resource import DataResource


class ProfilePluginYdataProfiling(Profiling):
    """
    Pandas profiling implementation of profiling plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.resource = None
        self.exec_multiprocess = True

    def setup(
        self,
        data_reader: NativeReader,
        resource: DataResource,
        exec_args: dict,
    ) -> None:
        """
        Set plugin resource.
        """
        self.data_reader = data_reader
        self.resource = resource
        self.exec_args = exec_args

    @exec_decorator
    def profile(self) -> ProfileReport:
        """
        Generate ydata_profiling profile.
        """
        data = self.data_reader.fetch_data(self.resource.path)
        profile = ProfileReport(data, lazy=False, **self.exec_args)
        return ProfileReport().loads(profile.dumps())

    @exec_decorator
    def render_nefertem(self, result: Result) -> NefertemProfile:
        """
        Return a NefertemProfile.
        """
        exec_err = result.errors
        duration = result.duration

        if exec_err is None:
            # Profile preparation
            json_str = result.artifact.to_json()
            json_str = json_str.replace("NaN", "null")
            full_profile = json.loads(json_str)

            # Short profile args
            args = {k: full_profile.get(k, {}) for k in PROFILE_COLUMNS}

            # Variables overwriting by filtering
            var = args.get("variables", {})
            for key in var:
                args["variables"][key] = {k: var[key][k] for k in PROFILE_FIELDS}

            # Get fields, stats and duration
            fields = args.get("variables", {})
            stats = args.get("table", {})

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
            filename = self._fn_profile.format("ydata.json")
            artifacts.append(self.get_render_tuple(_object, filename))
        else:
            string_html = result.artifact.to_html()
            strio_html = write_bytesio(string_html)
            html_filename = self._fn_profile.format("ydata.html")
            artifacts.append(self.get_render_tuple(strio_html, html_filename))

            string_json = result.artifact.to_json()
            string_json = string_json.replace("NaN", "null")
            strio_json = write_bytesio(string_json)
            json_filename = self._fn_profile.format("ydata.json")
            artifacts.append(self.get_render_tuple(strio_json, json_filename))

        return artifacts

    @staticmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """
        return ydata_profiling.__name__

    @staticmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """
        return ydata_profiling.__version__
