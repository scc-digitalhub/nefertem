import importlib

import evidently
from evidently.report import Report
from nefertem.metadata.nefertem import NefertemProfile

from nefertem.metadata.nefertem import NefertemProfileMetric
from nefertem.plugins.profiling.base import Profiling
from nefertem.plugins.profiling.evidently.metrics import MetricEvidently
from nefertem.plugins.utils import Result, exec_decorator
from nefertem.readers.base.file import FileReader
from nefertem.resources.data_resource import DataResource
from nefertem.utils.io_utils import write_bytesio


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
