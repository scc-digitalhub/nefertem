"""
Evidently implementation of profiling plugin.
"""
from __future__ import annotations

import importlib
import typing

import evidently
from evidently.report import Report
from pydantic import BaseModel, Field

from nefertem.metadata.reports.profile import NefertemProfile, NefertemProfileMetric
from nefertem.plugins.profiling.base import Metric, Profiling, ProfilingPluginBuilder
from nefertem.plugins.utils.plugin_utils import exec_decorator
from nefertem.utils.commons import BASE_FILE_READER
from nefertem.utils.io_utils import write_bytesio

if typing.TYPE_CHECKING:
    from nefertem.plugins.utils.plugin_utils import Result
    from nefertem.readers.base.file import FileReader
    from nefertem.resources.data_resource import DataResource


####################
# PLUGIN
####################


class ProfilePluginEvidently(Profiling):
    """
    Evidently implementation of profiling plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.resource = None
        self.reference_resource = None
        self.exec_multiprocess = True

    def setup(
        self,
        data_reader: FileReader,
        resource: DataResource,
        metric: MetricEvidently,
        exec_args: dict,
        reference_data_reader: FileReader = None,
        reference_resource: DataResource = None,
    ) -> None:
        """
        Set plugin resource.
        """
        self.data_reader = data_reader
        self.reference_data_reader = reference_data_reader
        self.resource = resource
        self.reference_resource = reference_resource
        self.metric = metric
        self.exec_args = exec_args

    @exec_decorator
    def profile(self) -> Report:
        """
        Generate evidently profile.
        """
        data = self.data_reader.fetch_data(self.resource.path)
        reference_data = (
            None
            if self.reference_resource is None
            else self.reference_data_reader.fetch_data(self.reference_resource.path)
        )

        metrics = self._rebuild_metrics()
        report = Report(metrics=metrics)
        report.run(current_data=data, reference_data=reference_data)
        return report

    def _rebuild_metrics(self) -> list[any]:
        """
        Rebuild metrics converting to Evidently metrics.
        """
        res = []
        for m in self.metric.metrics:
            check = m.type
            module_name, class_name = check.rsplit(".", 1)
            _class = getattr(importlib.import_module(module_name), class_name)
            if m.values:
                res.append(_class(**m.values))
            else:
                res.append(_class())
        return res

    @exec_decorator
    def render_nefertem(self, result: Result) -> NefertemProfile:
        """
        Return a NefertemProfile.
        """
        exec_err = result.errors
        duration = result.duration

        field_metrics = {}
        res_metrics = []
        stats = {}
        fields = {}
        if exec_err is None:
            # Profile preparation
            full_profile = result.artifact.as_dict()
            metrics = full_profile.get("metrics", [])
            for m in metrics:
                metric_name = m.get("metric")
                value = m.get("result", {})
                if "column_name" in value:
                    field = value.get("column_name")
                    list = field_metrics.get(field, [])
                    del value["column_name"]
                    list.append(NefertemProfileMetric(metric_name, metric_name, "evidently", None, value))
                    field_metrics[field] = list
                else:
                    res_metrics.append(NefertemProfileMetric(metric_name, metric_name, "evidently", None, value))

        return NefertemProfile(
            self.get_lib_name(), self.get_lib_version(), duration, stats, fields, res_metrics, field_metrics
        )

    @exec_decorator
    def render_artifact(self, result: Result) -> list[tuple]:
        """
        Return a rendered profile ready to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
            filename = self._fn_profile.format("evidently.json")
            artifacts.append(self.get_render_tuple(_object, filename))
        else:
            # string_html = result.artifact.to_html()
            #     strio_html = write_bytesio(string_html)
            html_filename = self._fn_profile.format("evidently.html")
            string_html = result.artifact.get_html()
            strio_html = write_bytesio(string_html)
            artifacts.append(self.get_render_tuple(strio_html, html_filename))

            string_json = result.artifact.json()
            string_json = string_json.replace("NaN", "null")
            strio_json = write_bytesio(string_json)
            json_filename = self._fn_profile.format("evidently.json")
            artifacts.append(self.get_render_tuple(strio_json, json_filename))

        return artifacts

    @staticmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """
        return evidently.__name__

    @staticmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """
        return evidently.__version__


####################
# BUILDER
####################


class ProfileBuilderEvidently(ProfilingPluginBuilder):
    """
    Evidently profile plugin builder.
    """

    def build(self, resources: list[DataResource], metrics: list[Metric] | None = None) -> list[ProfilePluginEvidently]:
        """
        Build a plugin for every metric element.
        """
        if metrics is None or len(metrics) == 0:
            return []

        f_metrics = self._filter_metrics(metrics)
        plugins = []
        for metric in f_metrics:
            data_reader = None
            curr_resource = None
            ref_data_reader = None
            ref_resource = None
            for resource in resources:
                if resource.name == metric.resource:
                    store = self._get_resource_store(resource)
                    data_reader = self._get_data_reader(BASE_FILE_READER, store)
                    curr_resource = resource
                elif resource.name == metric.reference_resource:
                    store = self._get_resource_store(resource)
                    ref_data_reader = self._get_data_reader(BASE_FILE_READER, store)
                    ref_resource = resource

            if curr_resource is not None:
                plugin = ProfilePluginEvidently()
                plugin.setup(data_reader, resource, metric, self.exec_args, ref_data_reader, ref_resource)
                plugins.append(plugin)

        return plugins

    @staticmethod
    def _filter_metrics(metrics: list[Metric]) -> list[Metric]:
        """
        Filter out MetricEvidently.
        """
        if metrics is None:
            return []
        return [m for m in metrics if m.type == evidently]

    def destroy(self) -> None:
        """
        Destory plugins.
        """


####################
# METRIC
####################


class Element(BaseModel):
    """
    Evidently single test
    """

    type: str
    """Evidently test/metric type (fully qualified class name)."""
    values: dict | None = None
    """Custom parameters for the test/metric."""


class MetricEvidently(Metric):
    """
    Evidently metric input model.
    """

    type: str = Field("evidently", Literal=True)
    """Metric input type ("Evidently")."""

    resource: str
    """Resource to profile."""

    reference_resource: str | None = None
    """Resource to use as reference."""

    metrics: list[Element]
    """Evidently tests."""
