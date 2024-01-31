"""
SQLAlchemy implementation of validation plugin.
"""
from __future__ import annotations

import typing

import sqlalchemy
from nefertem_core.plugins.utils import RenderTuple, exec_decorator
from nefertem_validation.metadata.report import NefertemReport
from nefertem_validation.plugins.plugin import ValidationPlugin
from nefertem_validation.plugins.utils import get_errors, parse_error_report, render_error_type
from nefertem_validation_sqlalchemy.utils import (
    ValidationReport,
    evaluate_validity,
    return_first_value,
    return_head,
    return_length,
)

if typing.TYPE_CHECKING:
    from nefertem_core.plugins.utils import Result
    from nefertem_validation_sqlalchemy.constraint import ConstraintSqlAlchemy
    from nefertem_validation_sqlalchemy.reader import PandasDataFrameSQLReader


class ValidationPluginSqlAlchemy(ValidationPlugin):
    """
    SQLAlchemy implementation of validation plugin.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        super().__init__()
        self.exec_multiprocess = True

    def setup(
        self,
        data_reader: PandasDataFrameSQLReader,
        constraint: ConstraintSqlAlchemy,
        error_report: str,
    ) -> None:
        """
        Setup plugin.

        Parameters
        ----------
        data_reader : PandasDataFrameSQLReader
            Data reader.
        constraint : ConstraintSqlAlchemy
            Constraint to validate resource in db.
        error_report : str
            Error report modality.
        """
        self.data_reader = data_reader
        self.constraint = constraint
        self.error_report = error_report

        # Set filter function according to check type
        if self.constraint.check == "value":
            self.filter_fnc = return_first_value
        elif self.constraint.check == "rows":
            self.filter_fnc = return_length

    @exec_decorator
    def validate(self) -> dict:
        """
        Generate a validation report.

        Returns
        -------
        ValidationReport
            ValidationReport object.
        """
        try:
            # Fetch data from db
            data = self.data_reader.fetch_data(self.constraint.name, self.constraint.query)

            # Filter data
            value = self.filter_fnc(data)

            # Evaluate validity
            valid, errors = evaluate_validity(value, self.constraint.expect, self.constraint.value)

            # Return report
            result = return_head(data)
            return ValidationReport(result, valid, errors)
        except Exception as ex:
            raise ex

    @exec_decorator
    def render_nefertem(self, result: Result) -> RenderTuple:
        """
        Return a NefertemReport ready to be persisted as metadata.

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
        constraint = self.constraint.dict()
        errors = {}

        if exec_err is None:
            valid = result.artifact.valid
            if not valid:
                total_count = 1
                errors_list = [render_error_type("sql-check-error")]
                parsed_error_list = parse_error_report(errors_list, self.error_report)
                errors = get_errors(total_count, parsed_error_list)
        else:
            self.logger.error(f"Execution error {str(exec_err)} for plugin {self.id}")
            valid = False

        obj = NefertemReport(
            **self.get_framework(),
            duration=duration,
            constraint=constraint,
            valid=valid,
            errors=errors,
        )
        filename = f"nefertem_report_{self.id}.json"
        return RenderTuple(obj, filename)

    @exec_decorator
    def render_artifact(self, result: Result) -> list[RenderTuple]:
        """
        Return a rendered report ready to be persisted as artifact.

        Parameters
        ----------
        result : Result
            Execution result.

        Returns
        -------
        list[RenderTuple]
            Rendered object.
        """
        if result.artifact is None:
            obj = {"errors": result.errors}
        else:
            obj = result.artifact.to_dict()
        filename = f"sqlalchemy_report_{self.id}.json"
        return [RenderTuple(obj, filename)]

    @staticmethod
    def framework_name() -> str:
        """
        Get library name.

        Returns
        -------
        str
            Library name.
        """
        return sqlalchemy.__name__

    @staticmethod
    def framework_version() -> str:
        """
        Get library version.

        Returns
        -------
        str
            Library version.
        """
        return sqlalchemy.__version__
