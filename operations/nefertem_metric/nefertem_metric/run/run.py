"""
Run handler module.
"""
from typing import Any

from nefertem_metric.metadata.report import NefertemMetricReport

from nefertem.metadata.blob import BlobLog
from nefertem.run.run import Run
from nefertem.utils.commons import RESULT_FRAMEWORK, RESULT_NEFERTEM, RESULT_RENDERED


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
        metrics = self.run_handler.get_item(RESULT_FRAMEWORK)
        if metrics:
            return metrics

        self.run_handler.run(self.run_info.resources, metrics)
        return self.run_handler.get_item(RESULT_FRAMEWORK)

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
        metrics = self.run_handler.get_item(RESULT_NEFERTEM)
        if metrics:
            return metrics

        self.run_handler.run(self.run_info.resources, metrics)
        return self.run_handler.get_item(RESULT_NEFERTEM)

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
        for obj in self.run_handler.get_item(RESULT_NEFERTEM):
            metadata = BlobLog(*self._get_base_args(), obj.to_dict()).to_dict()
            self._log_metadata(metadata, "metric")

    def persist_metric(self) -> None:
        """
        Persist frameworks metrics.

        Returns
        -------
        None
        """
        for obj in self.run_handler.get_item(RESULT_RENDERED):
            self._persist_artifact(obj.object, self._render_artifact_name(obj.filename))
