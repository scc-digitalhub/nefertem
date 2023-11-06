"""
Run handler module.
"""
from typing import Any

from nefertem_validation.metadata.report import NefertemReport

from nefertem.metadata.blob import BlobLog
from nefertem.run.run import Run
from nefertem.utils.commons import RESULT_FRAMEWORK, RESULT_NEFERTEM, RESULT_RENDERED


class RunValidation(Run):
    """
    Run validation extension.

    Methods
    -------
    validate
        Execute validation on resources.
    validate_framework
        Execute validation on resources with validation frameworks.
    validate_nefertem
        Execute validation on resources with Nefertem.
    log_report
        Log NefertemReport.
    persist_report
        Persist frameworks reports.
    """

    def validate_framework(self, constraints: list[dict], error_report: str | None = "partial") -> list[Any]:
        """
        Execute validation on resources with validation frameworks.

        Parameters
        ----------
        constraints : list[dict]
            list of constraint to validate resources.
        error_report : str
            Flag to render the error output of the nefertem report.
            Accepts 'count', 'partial' or 'full'.
            'count' returns the errors count of the validation,
            'partial' return the errors count and a list of errors (max 100),
            'full' returns errors count and the list of all encountered errors.

        Returns
        -------
        list[Any]
            Return a list of framework results.
        """
        reports = self.run_handler.get_item(RESULT_FRAMEWORK)
        if reports:
            return reports

        self.run_handler.run(self.run_info.resources, constraints, error_report)
        return self.run_handler.get_item(RESULT_FRAMEWORK)

    def validate_nefertem(self, constraints: list[dict], error_report: str | None = "partial") -> list[NefertemReport]:
        """
        Execute validation on resources with Nefertem.

        Parameters
        ----------
        constraints : list[dict]
            list of constraint to validate resources.
        error_report : str
            Flag to render the error output of the nefertem report.
            Accepts 'count', 'partial' or 'full'.
            'count' returns the errors count of the validation,
            'partial' return the errors count and a list of errors (max 100),
            'full' returns errors count and the list of all encountered errors.

        Returns
        -------
        list[NefertemReport]
            Return a list of "NefertemReport".
        """
        reports = self.run_handler.get_item(RESULT_NEFERTEM)
        if reports:
            return reports

        self.run_handler.run(self.run_info.resources, constraints, error_report)
        return self.run_handler.get_item(RESULT_NEFERTEM)

    def validate(self, constraints: list[dict], error_report: str | None = "partial") -> Any:
        """
        Execute validation on resources.

        Parameters
        ----------
        constraints : list[dict]
            list of constraint to validate resources.
        error_report : str
            Flag to render the error output of the nefertem report.
            Accepts 'count', 'partial' or 'full'.
            'count' returns the errors count of the validation,
            'partial' return the errors count and a list of errors (max 100),
            'full' returns errors count and the list of all encountered errors.
        only_nt : bool
            Flag to return only the Nefertem report.

        Returns
        -------
        Any
            Return a list of "NefertemReport" and the corresponding list of framework results.

        """
        return (self.validate_framework(constraints, error_report), self.validate_nefertem(constraints, error_report))

    def log_report(self) -> None:
        """
        Log NefertemReport.

        Returns
        -------
        None
        """
        for obj in self.run_handler.get_item(RESULT_NEFERTEM):
            metadata = BlobLog(*self._get_base_args(), obj.to_dict()).to_dict()
            self._log_metadata(metadata, "report")

    def persist_report(self) -> None:
        """
        Persist frameworks reports.

        Returns
        -------
        None
        """
        for obj in self.run_handler.get_item(RESULT_RENDERED):
            self._persist_artifact(obj.object, self._render_artifact_name(obj.filename))
