"""
GreatExpectations implementation of profiling plugin.
"""
from copy import deepcopy
from typing import List, Optional

import great_expectations as ge
from great_expectations.core.expectation_suite import ExpectationSuite
from great_expectations.profile.user_configurable_profiler import (
    UserConfigurableProfiler,
)

from nefertem.metadata.nefertem_reports import NefertemProfile
from nefertem.plugins.profiling.profiling_plugin import Profiling, ProfilingPluginBuilder
from nefertem.plugins.utils.great_expectations_utils import (
    get_great_expectations_validator,
)
from nefertem.plugins.utils.plugin_utils import exec_decorator
from nefertem.utils.commons import (
    LIBRARY_GREAT_EXPECTATIONS,
    PANDAS_DATAFRAME_FILE_READER,
)


class ProfilePluginGreatExpectations(Profiling):
    """
    SQLAlchemy with GreatExpectations implementation of validation plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.resource = None
        self.exec_multiprocess = True

    def setup(
        self,
        data_reader: "NativeReader",
        resource: "DataResource",
        exec_args: dict,
    ) -> None:
        """
        Set plugin resource.
        """
        self.data_reader = data_reader
        self.resource = resource
        self.exec_args = exec_args

    @exec_decorator
    def profile(self) -> dict:
        """
        Profile a Data Resource.
        """
        data = self.data_reader.fetch_data(self.resource.path)
        validator = get_great_expectations_validator(
            data, str(self.resource.name), str(self.resource.title)
        )
        profiler = UserConfigurableProfiler(profile_dataset=validator)
        result = profiler.build_suite()
        return ExpectationSuite(**result.to_json_dict())

    @exec_decorator
    def render_nefertem(self, result: "Result") -> NefertemProfile:
        """
        Return a NefertemProfile.
        """
        exec_err = result.errors
        duration = result.duration
        metrics = []
        field_metrics = {}

        if exec_err is None:
            res = deepcopy(result.artifact).to_json_dict()
            fields = {"fields": list(res.get("meta", {}).get("columns", {}).keys())}
            stats = {"stats": list(res.get("expectations"))}
        else:
            self.logger.error(f"Execution error {str(exec_err)} for plugin {self._id}")
            fields = {}
            stats = {}

        return NefertemProfile(
            self.get_lib_name(), self.get_lib_version(), duration, stats, fields, metrics, field_metrics
        )

    @exec_decorator
    def render_artifact(self, result: "Result") -> List[tuple]:
        """
        Return a rendered report ready to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
        else:
            _object = result.artifact.to_json_dict()
        filename = self._fn_profile.format(f"{LIBRARY_GREAT_EXPECTATIONS}.json")
        artifacts.append(self.get_render_tuple(_object, filename))
        return artifacts

    @staticmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """
        return ge.__name__

    @staticmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """
        return ge.__version__


class ProfileBuilderGreatExpectations(ProfilingPluginBuilder):
    """
    Profile plugin builder.
    """

    def build(
        self, 
        resources: List["DataResource"],
        metrics: Optional[List] = None
    ) -> List[ProfilePluginGreatExpectations]:
        """
        Build a plugin. Metrics are not supported
        """
        if metrics is not None and len(metrics) > 0:
            return []
        plugins = []
        for res in resources:
            resource = self._get_resource_deepcopy(res)
            store = self._get_resource_store(resource)
            data_reader = self._get_data_reader(PANDAS_DATAFRAME_FILE_READER, store)
            plugin = ProfilePluginGreatExpectations()
            plugin.setup(data_reader, resource, self.exec_args)
            plugins.append(plugin)
        return plugins

    @staticmethod
    def _filter_metrics(metrics: List["Metric"]) -> List["Metric"]:
        ...

    def destroy(self) -> None:
        ...
