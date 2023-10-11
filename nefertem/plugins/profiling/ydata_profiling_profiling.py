"""
Pandas profiling implementation of profiling plugin.
"""
import json
from typing import List, Optional

import ydata_profiling
from ydata_profiling import ProfileReport

from nefertem.metadata.nefertem_reports import NefertemProfile, NefertemProfileMetric
from nefertem.plugins.profiling.profiling_plugin import Profiling, ProfilingPluginBuilder
from nefertem.plugins.utils.plugin_utils import exec_decorator
from nefertem.utils.commons import (
    LIBRARY_YDATA_PROFILING,
    PANDAS_DATAFRAME_FILE_READER,
)
from nefertem.utils.io_utils import write_bytesio


# Columns/fields to parse from profile
PROFILE_COLUMNS = ["analysis", "table", "variables"]
PROFILE_FIELDS = [
    "n_distinct",
    "p_distinct",
    "is_unique",
    "n_unique",
    "p_unique",
    "type",
    "hashable",
    "n_missing",
    "n",
    "p_missing",
    "count",
    "memory_size",
]
PROFILE_DATASET_METRICS = [
    "n",
    "n_var",
    "memory_size",
    "record_size",
    "n_cells_missing",
    "n_vars_with_missing",
    "n_vars_all_missing",
    "p_cells_missing",
    "n_duplicates",
    "p_duplicates"
]
PROFILE_FIELD_METRICS = [
    "n_distinct",
    "p_distinct",
    "is_unique",
    "n_unique",
    "p_unique",
    "type",
    "hashable",
    "n_missing",
    "n",
    "p_missing",
    "count",
    "memory_size",
    "n_negative",
    "p_negative",
    "n_infinite",
    "n_zeros",
    "mean",
    "std",
    "variance",
    "min",
    "max",
    "kurtosis",
    "skewness",
    "sum",
    "mad",
    "chi_squared_statistic",
    "chi_squared_pvalue",
    "range",
    "iqr",
    "cv",
    "p_zeros",
    "p_infinite"
]

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
    def profile(self) -> ProfileReport:
        """
        Generate ydata_profiling profile.
        """
        data = self.data_reader.fetch_data(self.resource.path)
        profile = ProfileReport(data, lazy=False, **self.exec_args)
        return ProfileReport().loads(profile.dumps())

    @exec_decorator
    def render_nefertem(self, result: "Result") -> NefertemProfile:
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
            metrics, field_metrics = self._extract_metrics(args)
        else:
            self.logger.error(f"Execution error {str(exec_err)} for plugin {self._id}")
            fields = {}
            stats = {}
            metrics = []
            field_metrics = {}

        return NefertemProfile(
            self.get_lib_name(), self.get_lib_version(), duration, stats, fields, metrics, field_metrics
        )

    def _extract_metrics(self, args) -> (list, dict):
        metrics = []
        field_metrics = {}
        table = args.get("table", {})
        var = args.get("variables", {})

        for m in PROFILE_DATASET_METRICS:
            metrics.append(
                NefertemProfileMetric(
                    m, m, "ydata_profiling", None, table[m]
                ) 
            )
        for key in var:
            field_metrics[key] = []
            for m in PROFILE_FIELD_METRICS:
                v = var.get(key, {}).get(m, None)
                if v is not None:
                    field_metrics[key].append(
                        NefertemProfileMetric(
                            m, m, "ydata_profiling", None, v
                        ) 
                    )
        return (metrics, field_metrics)

    @exec_decorator
    def render_artifact(self, result: "Result") -> List[tuple]:
        """
        Return a rendered profile ready to be persisted as artifact.
        """
        artifacts = []

        if result.artifact is None:
            _object = {"errors": result.errors}
            filename = self._fn_profile.format(f"{LIBRARY_YDATA_PROFILING}.json")
            artifacts.append(self.get_render_tuple(_object, filename))
        else:
            string_html = result.artifact.to_html()
            strio_html = write_bytesio(string_html)
            html_filename = self._fn_profile.format(f"{LIBRARY_YDATA_PROFILING}.html")
            artifacts.append(self.get_render_tuple(strio_html, html_filename))

            string_json = result.artifact.to_json()
            string_json = string_json.replace("NaN", "null")
            strio_json = write_bytesio(string_json)
            json_filename = self._fn_profile.format(f"{LIBRARY_YDATA_PROFILING}.json")
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


class ProfileBuilderYdataProfiling(ProfilingPluginBuilder):
    """
    Profile plugin builder.
    """

    def build(
        self, 
        resources: List["DataResource"],
        metrics: Optional[List] = None
    ) -> List[ProfilePluginYdataProfiling]:
        """
        Build a plugin.
        """
        if metrics is not None and len(metrics) > 0:
            return []
        plugins = []
        for res in resources:
            resource = self._get_resource_deepcopy(res)
            store = self._get_resource_store(resource)
            data_reader = self._get_data_reader(PANDAS_DATAFRAME_FILE_READER, store)
            plugin = ProfilePluginYdataProfiling()
            plugin.setup(data_reader, resource, self.exec_args)
            plugins.append(plugin)
        return plugins

    @staticmethod
    def _filter_metrics(metrics: List["Metric"]) -> List["Metric"]:
        ...
        
    def destroy(self) -> None:
        """
        Destory plugins.
        """
