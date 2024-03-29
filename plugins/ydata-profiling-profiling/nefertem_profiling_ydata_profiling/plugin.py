"""
Pandas profiling implementation of profiling plugin.
"""
from __future__ import annotations

import json
import typing

import ydata_profiling
from nefertem_core.plugins.utils import RenderTuple, exec_decorator
from nefertem_core.utils.io_utils import write_bytesio
from nefertem_profiling.metadata.report import NefertemProfile
from nefertem_profiling.plugins.plugin import ProfilingPlugin
from nefertem_profiling_ydata_profiling.utils import PROFILE_COLUMNS, PROFILE_FIELDS
from ydata_profiling import ProfileReport

if typing.TYPE_CHECKING:
    from nefertem_core.plugins.utils import Result
    from nefertem_core.resources.data_resource import DataResource
    from nefertem_profiling_ydata_profiling.reader import PandasDataFrameFileReader


class ProfilingPluginYdataProfiling(ProfilingPlugin):
    """
    Pandas profiling implementation of profiling plugin.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        super().__init__()
        self.resource = None
        self.exec_multiprocess = True

    def setup(
        self,
        data_reader: PandasDataFrameFileReader,
        resource: DataResource,
        exec_args: dict,
    ) -> None:
        """
        Setup plugin.

        Parameters
        ----------
        data_reader : PandasDataFrameFileReader
            Data reader.
        resource : DataResource
            Data resource to be profiled.
        exec_args : dict
            Execution arguments for ProfileReport.

        Returns
        -------
        None
        """
        self.data_reader = data_reader
        self.resource = resource
        self.exec_args = exec_args

    @exec_decorator
    def profile(self) -> ProfileReport:
        """
        Generate ydata_profiling profile.

        Returns
        -------
        ProfileReport
            ProfileReport object.
        """
        data = self.data_reader.fetch_data(self.resource.path)
        profile = ProfileReport(data, lazy=False, **self.exec_args)
        return ProfileReport().loads(profile.dumps())

    @exec_decorator
    def render_nefertem(self, result: Result) -> RenderTuple:
        """
        Return a NefertemProfile ready to be persisted as metadata.

        Parameters
        ----------
        result : Result
            Execution result.

        Returns
        -------
        RenderTuple
            Rendered object.
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
            self.logger.error(f"Execution error {str(exec_err)} for plugin {self.id}")
            fields = {}
            stats = {}

        obj = NefertemProfile(
            **self.get_framework(),
            duration=duration,
            stats=stats,
            fields=fields,
        )
        filaname = f"nefertem_profile_{self.id}.json"
        return RenderTuple(obj, filaname)

    @exec_decorator
    def render_artifact(self, result: Result) -> list[RenderTuple]:
        """
        Return a rendered profile ready to be persisted as artifact.

        Parameters
        ----------
        result : Result
            Execution result.

        Returns
        -------
        list[tuple]
            List of RenderTuple.
        """
        artifacts = []

        if result.artifact is None:
            obj = {"errors": result.errors}
            filename = f"ydata_profile_{self.id}.json"
            artifacts.append(RenderTuple(obj, filename))
        else:
            # HTML version
            string_html = result.artifact.to_html()
            strio_html = write_bytesio(string_html)
            html_filename = f"ydata_profile_{self.id}.html"
            artifacts.append(RenderTuple(strio_html, html_filename))

            # JSON version
            string_json = result.artifact.to_json().replace("NaN", "null")
            strio_json = write_bytesio(string_json)
            json_filename = f"ydata_profile_{self.id}.json"
            artifacts.append(RenderTuple(strio_json, json_filename))

        return artifacts

    @staticmethod
    def framework_name() -> str:
        """
        Get library name.

        Returns
        -------
        str
            Library name.
        """
        return ydata_profiling.__name__

    @staticmethod
    def framework_version() -> str:
        """
        Get library version.

        Returns
        -------
        str
            Library version.
        """
        return ydata_profiling.__version__
