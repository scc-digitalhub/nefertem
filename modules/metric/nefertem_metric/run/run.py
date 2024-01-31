"""
Run handler module.
"""
from __future__ import annotations

from typing import Any

from nefertem_core.metadata.blob import Blob
from nefertem_core.plugins.utils import ResultType
from nefertem_core.run.run import Run
from nefertem_metric.metadata.report import NefertemMetricReport


class RunMetric(Run):
    """
    Run metric extension.

    Methods
    -------
    metric
        Execute metric on resources.
    metric_framework
        Execute metric on resources with metric frameworks.
    metric_nefertem
        Execute metric on resources with Nefertem.
    log_metric
        Log NefertemMetricReports.
    persist_metric
        Persist frameworks metrics.
    """

    ############################
    # Metric
    ############################

    def metric_framework(self, metrics: list[dict]) -> list[Any]:
        """
        Execute metric on resources with metric frameworks.

        Parameters
        ----------
        metrics: list[dict]
            Optional list of metrics to evaluate over resources.

        Returns
        -------
        list[Any]
            Return a list of framework results.

        """
        metrics = self.run_handler.get_item(ResultType.FRAMEWORK.value)
        if metrics:
            return metrics

        self.run_handler.run(self.run_info.resources, metrics)
        return self.run_handler.get_item(ResultType.FRAMEWORK.value)

    def metric_nefertem(self, metrics: list[dict]) -> list[NefertemMetricReport]:
        """
        Execute metric on resources with Nefertem.

        Parameters
        ----------
        metrics: list[dict]
            Optional list of metrics to evaluate over resources.

        Returns
        -------
        list[NefertemMetricReport]
            Return a list of NefertemMetricReport.

        """
        metrics = self.run_handler.get_item(ResultType.NEFERTEM.value)
        if metrics:
            return metrics

        self.run_handler.run(self.run_info.resources, metrics)
        return self.run_handler.get_item(ResultType.NEFERTEM.value)

    def metric(self, metrics: list[dict]) -> tuple[list[Any], list[NefertemMetricReport]]:
        """
        Execute metric on resources.

        Parameters
        ----------
        metrics: list[dict]
            Optional list of metrics to evaluate over resources.

        Returns
        -------
        Any
            Return a list of NefertemMetricReport and the corresponding list of framework results.

        """
        return self.metric_framework(metrics), self.metric_nefertem(metrics)

    def log_metric(self) -> None:
        """
        Log NefertemMetricReports.

        Returns
        -------
        None
        """
        for obj in self.run_handler.get_item(ResultType.NEFERTEM.value):
            metadata = Blob(*self._get_base_args(), obj.object.to_dict()).to_dict()
            self._log_metadata(metadata, obj.filename)

    def persist_metric(self) -> None:
        """
        Persist frameworks metrics.

        Returns
        -------
        None
        """
        for obj in self.run_handler.get_item(ResultType.RENDERED.value):
            self._persist_artifact(obj.object, obj.filename)
