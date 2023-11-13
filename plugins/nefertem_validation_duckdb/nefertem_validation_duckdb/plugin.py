"""
DuckDB implementation of validation plugin.
"""
from __future__ import annotations

import typing
from typing import Any

import duckdb
from nefertem_validation.metadata.report import NefertemReport
from nefertem_validation.plugins.plugin import ValidationPlugin
from nefertem_validation_duckdb.utils import ValidationReport, evaluate_validity

from nefertem.plugins.utils import exec_decorator

if typing.TYPE_CHECKING:
    from nefertem_validation_duckdb.constraint import ConstraintDuckDB
    from nefertem_validation_duckdb.reader import PandasDataFrameDuckDBReader

    from nefertem.plugins.utils import Result


class ValidationPluginDuckDB(ValidationPlugin):
    """
    DuckDB implementation of validation plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.db = None
        self.exec_multiprocess = True

    def setup(
        self,
        data_reader: PandasDataFrameDuckDBReader,
        db: str,
        constraint: ConstraintDuckDB,
        error_report: str,
        exec_args: dict,
    ) -> None:
        """
        Set plugin resource.
        """
        self.data_reader = data_reader
        self.db = db
        self.constraint = constraint
        self.error_report = error_report
        self.exec_args = exec_args

    @exec_decorator
    def validate(self) -> dict:
        """
        Validate a Data Resource.
        """
        try:
            data = self.data_reader.fetch_data(self.db, self.constraint.query)
            value = self._filter_result(data)
            valid, errors = evaluate_validity(value, self.constraint.expect, self.constraint.value)
            result = self.data_reader.return_head(data)
            return ValidationReport(result, valid, errors)
        except Exception as ex:
            raise ex

    def _filter_result(self, data: Any) -> Any:
        """
        Return value or size of DataFrame for SQL checks.
        """
        if self.constraint.check == "value":
            return self.data_reader.return_first_value(data)
        elif self.constraint.check == "rows":
            return self.data_reader.return_length(data)

    @exec_decorator
    def render_nefertem(self, result: Result) -> NefertemReport:
        """
        Return a NefertemReport.
        """
        exec_err = result.errors
        duration = result.duration
        constraint = self.constraint.model_dump()
        errors = {}

        if exec_err is None:
            valid = result.artifact.valid
            if not valid:
                total_count = 1
                errors_list = [self._render_error_type("sql-check-error")]
                parsed_error_list = self._parse_error_report(errors_list)
                errors = self._get_errors(total_count, parsed_error_list)
        else:
            self.logger.error(f"Execution error {str(exec_err)} for plugin {self._id}")
            valid = False

        return NefertemReport(
            self.framework_name(),
            self.framework_version(),
            duration,
            constraint,
            valid,
            errors,
        )

    @exec_decorator
    def render_artifact(self, result: Result) -> list[tuple]:
        """
        Return a rendered report ready to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
        else:
            _object = result.artifact.to_dict()
        filename = self._fn_report.format("duckdb.json")
        artifacts.append(self._get_render_tuple(_object, filename))
        return artifacts

    @staticmethod
    def framework_name() -> str:
        """
        Get library name.
        """
        return duckdb.__name__

    @staticmethod
    def framework_version() -> str:
        """
        Get library version.
        """
        return duckdb.__version__
